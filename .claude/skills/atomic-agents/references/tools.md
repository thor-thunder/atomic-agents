# Tools (`BaseTool`)

`BaseTool` uses PEP 695 generics. Declare input/output schemas as type parameters; the
framework reads them back and exposes `self.input_schema` / `self.output_schema`.

```python
from pydantic import Field
from atomic_agents import BaseIOSchema, BaseTool, BaseToolConfig

class CalculatorInput(BaseIOSchema):
    """Arithmetic expression to evaluate."""
    expression: str = Field(..., description="Python-style arithmetic, e.g. '2 + 2 * 3'.")

class CalculatorOutput(BaseIOSchema):
    """Result of evaluating the expression."""
    result: float = Field(..., description="Numeric result.")

class CalculatorTool(BaseTool[CalculatorInput, CalculatorOutput]):
    """Evaluate simple arithmetic expressions safely."""
    def run(self, params: CalculatorInput) -> CalculatorOutput:
        ...  # return CalculatorOutput(result=...)
```

Do not assign `input_schema`/`output_schema` as class attributes — the generics carry the
types. `self.tool_name`/`self.tool_description` default to the input schema's title and
docstring; override with `BaseToolConfig(title=..., description=...)`.

## Config, auth, env vars

```python
import os
from atomic_agents import BaseToolConfig

class WeatherConfig(BaseToolConfig):
    api_key: str = Field(default_factory=lambda: os.environ.get("WEATHER_API_KEY", ""),
                         description="API key for the weather service.")
    timeout: float = Field(default=15.0, ge=1.0, le=120.0, description="Request timeout (s).")
```

Secrets come from the environment — never hardcode. Timeouts/retries belong in config.

## `run()` / `run_async()` contract

- `def run(self, params: InputSchema) -> OutputSchema` — abstract, must implement.
- For async-first tools add `async def run_async(...)` (the framework calls `run_async`, **not** `arun`).
- Return an `OutputSchema` instance, never raw dicts.
- Convert external failures (HTTP status, DB result) into a typed failure output (see schemas.md).

## Integrating tools with agents

Single-tool agent — output schema *is* the tool input schema:
```python
agent = AtomicAgent[UserQuery, CalculatorInput](config=config)
call = agent.run(UserQuery(question="What's 23 times 47?"))   # LLM picks args
result = CalculatorTool().run(call)                            # host runs the tool
```

Router agent — pick among tools via a discriminated union (`ToolChoice` with
`Union[CalcCall, SearchCall]`). Working example: `atomic-examples/orchestration-agent/`.

## MCP interop

```python
from atomic_agents.connectors.mcp import fetch_mcp_tools, MCPTransportType
tools = fetch_mcp_tools(transport=MCPTransportType.HTTP_STREAM, endpoint="https://server/mcp")
```

Transport values: `SSE`, `HTTP_STREAM`, `STDIO` — **not** `STREAMABLE_HTTP`. Async variants:
`fetch_mcp_tools_async`, plus `MCPFactory`. Example: `atomic-examples/mcp-agent/`.

## Prebuilt tools (Atomic Forge)

`atomic download calculator`, `atomic download tavily_search`, etc. Read
`atomic-forge/tools/calculator/tool/calculator.py` (minimal) and `.../searxng_search/`
(HTTP-backed, dual sync/async) as reference implementations.

## Common mistakes

- `input_schema = ...` as a class attribute instead of generics.
- Returning dicts/primitives from `run()`.
- Raising on routine failures (rate limits, not-found) — model them as typed output.
- Missing timeout on HTTP/DB calls.
- `MCPTransportType.STREAMABLE_HTTP` (use `HTTP_STREAM`).
