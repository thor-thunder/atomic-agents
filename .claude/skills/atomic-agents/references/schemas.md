# Schemas (`BaseIOSchema`)

`BaseIOSchema` is a Pydantic `BaseModel` plus a metaclass hook that **fails at
class-definition time** if the class has no (non-whitespace) docstring. The docstring
becomes the JSON schema `description` and the class name the `title` — Instructor uses
both when prompting the LLM, so write docstrings for the model.

```python
from pydantic import Field
from atomic_agents import BaseIOSchema

class SearchQuery(BaseIOSchema):
    """Parameters for a web search issued by the agent."""
    query: str = Field(..., description="Natural-language search query.")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum results to return.")
```

## Field patterns

```python
from typing import Optional, Literal
name: str = Field(..., description="Full legal name.")
nickname: Optional[str] = Field(default=None, description="Preferred nickname, if any.")
count: int = Field(default=10, ge=1, le=100, description="Items to return (1–100).")
sort: Literal["asc", "desc"] = Field(default="desc", description="Sort order.")
tags: list[str] = Field(default_factory=list, max_length=10, description="Tag filters (≤10).")
```

Prefer `Literal[...]` over `Enum` for closed sets — flatter JSON schema helps Instructor.

## Validators

```python
from pydantic import field_validator, model_validator

class DateRange(BaseIOSchema):
    """An inclusive date range."""
    start: date = Field(..., description="Start date (inclusive).")
    end: date = Field(..., description="End date (inclusive).")

    @model_validator(mode="after")
    def _ordered(self):
        if self.end < self.start:
            raise ValueError("end must be on or after start")
        return self
```

Validation errors surface as Instructor retries (up to `max_retries`) and fire the
`parse:error` hook.

## Discriminated unions & error-schema pattern

Model legitimate failure as a typed alternative output, not an exception:

```python
from typing import Literal, Union

class SearchSuccess(BaseIOSchema):
    """Successful search result."""
    results: list[str] = Field(..., description="Matching items.")

class SearchFailure(BaseIOSchema):
    """Search could not complete."""
    error: str = Field(..., description="Human-readable reason.")
    code: Literal["rate_limited", "no_results", "upstream_error"] = Field(..., description="Failure code.")

class SearchOutput(BaseIOSchema):
    """Search output — success or typed failure."""
    result: Union[SearchSuccess, SearchFailure] = Field(..., description="Outcome.")
```

## Common mistakes

- Forgetting the docstring (framework raises at import).
- Plain `BaseModel` — loses docstring enforcement and the schema override.
- `Field()` without `description=`.
- `Optional[str]` with no default — required-but-nullable, rarely intended.
- Over-broad types (`dict`, `Any`) — the LLM generates anything, Pydantic can't validate.
