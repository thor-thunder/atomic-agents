# Agents (`AtomicAgent` + `AgentConfig`)

## Config anatomy

```python
from atomic_agents import AgentConfig
from atomic_agents.context import ChatHistory, SystemPromptGenerator
from instructor import Mode

config = AgentConfig(
    client=client,                      # required: instructor-wrapped client
    model="gpt-5-mini",                 # required: model id
    history=ChatHistory(),              # optional: omit for stateless agents
    system_prompt_generator=SystemPromptGenerator(
        background=["You are a concise research assistant."],
        steps=["Understand the question.", "Search memory.", "Answer directly."],
        output_instructions=["Reply under 100 words.", "Cite sources when used."],
    ),
    system_role="system",               # None = no system prompt sent
    assistant_role="assistant",         # "model" for Gemini
    mode=Mode.TOOLS,                    # match the Instructor factory mode
    model_api_parameters={"temperature": 0.2, "max_tokens": 2048},
)
```

Match `mode` on `AgentConfig` to the Instructor factory mode (see providers.md).
`assistant_role` must be `"model"` for Gemini; everything else uses `"assistant"`.

## Creating the agent — generics carry runtime info

```python
from atomic_agents import AtomicAgent
agent = AtomicAgent[MyInput, MyOutput](config=config)
```

Do not rely on subclass-level `input_schema`/`output_schema` class attributes — the PEP
695 generic parameters are the source of truth.

## Execution modes

```python
out = agent.run(MyInput(...))                 # sync single-shot
out = agent.run()                             # rerun over existing history
out = await agent.run_async(MyInput(...))     # async single-shot
for partial in agent.run_stream(MyInput(...)):    ...   # sync streaming
async for partial in agent.run_async_stream(MyInput(...)): ...  # async streaming
```

Streaming partials are `MyOutput` instances with a subset of fields populated; validators
fire as fields appear, so keep them cheap.

## Token counting

```python
info = agent.get_context_token_count()
info.total          # tokens in the next request
info.utilization    # float in [0, 1], or None
```

Use this to gate long operations or decide when to summarize history.

## History & hooks (recap)

```python
history = ChatHistory()
agent.run(BasicChatInputSchema(chat_message="Q1"))
agent.run(BasicChatInputSchema(chat_message="Q2"))   # accumulates
agent.reset_history()

agent.register_hook("parse:error", lambda error: ...)
```

Hook events: `parse:error`, `completion:kwargs`, `completion:response`,
`completion:error`, `completion:last_attempt`.

## Context providers

```python
from atomic_agents.context import BaseDynamicContextProvider

class UserCtx(BaseDynamicContextProvider):
    def __init__(self):
        super().__init__(title="User Context")
        self.name = ""
    def get_info(self) -> str:
        return f"Current user: {self.name or 'anonymous'}"

agent.register_context_provider("user", UserCtx())
agent.context_providers["user"].name = "Alice"
```

## Common mistakes

- Forgetting `instructor.from_*` — structured outputs silently stop working.
- Raw `BaseModel` as I/O type — must be `BaseIOSchema`.
- `assistant_role="assistant"` with Gemini (needs `"model"`).
- `AgentConfig.mode` out of sync with the Instructor factory mode.
- Unbounded `ChatHistory` in a long-running service.
