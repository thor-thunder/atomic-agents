# Context Providers (`BaseDynamicContextProvider`)

A context provider injects a dynamic, runtime-computed section into the system prompt on
every `agent.run()`. Subclass `BaseDynamicContextProvider`, set a `title`, implement
`get_info()`.

```python
from atomic_agents.context import BaseDynamicContextProvider

class RAGContext(BaseDynamicContextProvider):
    def __init__(self, store):
        super().__init__(title="Retrieved Documents")
        self.store = store
        self.query = ""
    def get_info(self) -> str:
        docs = self.store.search(self.query, k=3)
        return "\n\n".join(f"[{d.id}] {d.text}" for d in docs)

ctx = RAGContext(store)
agent.register_context_provider("rag", ctx)
agent.context_providers["rag"].query = "refund policy"   # update before next run
reply = agent.run(UserQuery(...))
```

## Patterns

- **RAG:** fetch top-k chunks for the current query.
- **Time/session:** inject current datetime, user, locale.
- **Cached schema:** load a DB schema once, serve from memory.

## Rules

- `get_info()` runs on **every** `agent.run()` — keep it cheap; avoid blocking I/O, or cache.
- Update provider fields between runs to change what's injected.
- Register the **same** provider instance on multiple agents to share context (orchestration.md).
