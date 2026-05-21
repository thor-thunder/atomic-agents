# LLM Providers

Atomic Agents is provider-agnostic: any Instructor-supported client works. Read every key
from environment variables. Model IDs below are illustrative — names change; check the
provider docs or `atomic-examples/quickstart/quickstart/4_basic_chatbot_different_providers.py`.

## Provider matrix

| Provider | Instructor factory | `Mode` | `assistant_role` |
|---|---|---|---|
| OpenAI | `instructor.from_openai(OpenAI(...))` | `Mode.TOOLS` | `"assistant"` |
| Anthropic | `instructor.from_anthropic(Anthropic(...))` | `Mode.TOOLS` | `"assistant"` |
| Groq | `instructor.from_groq(Groq(...), mode=Mode.JSON)` | `Mode.JSON` | `"assistant"` |
| Ollama | `instructor.from_openai(OpenAI(base_url=..., api_key="ollama"), mode=Mode.JSON)` | `Mode.JSON` | `"assistant"` |
| Gemini | `instructor.from_genai(google.genai.Client(...), mode=Mode.GENAI_TOOLS)` | `Mode.GENAI_TOOLS` | `"model"` |
| OpenRouter | `instructor.from_openai(OpenAI(base_url=..., api_key=...))` | `Mode.TOOLS` | `"assistant"` |

Match `AgentConfig(mode=...)` to the factory mode.

## Anthropic (used by the orchestration squad)

```python
import os, instructor
from anthropic import Anthropic
client = instructor.from_anthropic(Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"]))
model = "claude-opus-4-7"     # leader; workers use "claude-sonnet-4-6"
api_params = {"max_tokens": 4096}   # Anthropic REQUIRES max_tokens on every call
```

## OpenAI

```python
client = instructor.from_openai(OpenAI(api_key=os.environ["OPENAI_API_KEY"]))
model = "gpt-5-mini"
api_params = {"reasoning_effort": "low", "max_tokens": 2048}
```

Reasoning models often prefer `system_role=None`.

## Picking a model

- **Parallel workers / tool use / routing** — `claude-sonnet-4-6` (this repo's worker tier);
  `claude-haiku-4-5` or `gpt-5-mini` for cheaper fan-out.
- **Hardest reasoning / leader synthesis** — `claude-opus-4-7` or reasoning-tier OpenAI.

## `model_api_parameters`

`max_tokens` (Anthropic requires), `temperature`, `top_p`, `reasoning_effort` (OpenAI
reasoning only). Unknown keys are forwarded verbatim.

## Installation

```toml
dependencies = ["atomic-agents>=2.7", "instructor[anthropic]>=1.14"]  # or [openai], [groq], [google-genai]
```
