# Two Models in Parallel — Opus Leader + Sonnet Workers

The framework puts the `client` and `model` on each agent's `AgentConfig`, so a single
program can mix model tiers: a **strong leader** (Opus 4.7) that plans and synthesizes,
plus several **fast workers** (Sonnet 4.6) that fan out in parallel.

This is the framework-level mirror of this repo's Claude Code orchestration squad
(`.claude/agents/orchestrator.md` on `model: opus`, five workers on `model: sonnet`,
driven by the `orchestrate` skill).

## Why split tiers

- **Cost/latency:** workers do the bulk of the work concurrently at the cheaper tier.
- **Quality where it counts:** the leader is reserved for hard reasoning — planning the
  decomposition and synthesizing worker outputs ("Opus is best when all is ready").
- **Escalation:** if a worker subtask turns out to be hard, promote *that* call to Opus.

## Wiring

```python
import os, asyncio, instructor
from anthropic import AsyncAnthropic
from atomic_agents import AtomicAgent, AgentConfig

client = instructor.from_anthropic(AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"]))

SONNET = "claude-sonnet-4-6"
OPUS   = "claude-opus-4-7"

def make_worker():
    # fresh agent (own history) per concurrent run — never share ChatHistory
    return AtomicAgent[WorkerIn, WorkerOut](
        config=AgentConfig(client=client, model=SONNET,
                           model_api_parameters={"max_tokens": 2048}))

leader = AtomicAgent[LeaderIn, LeaderOut](
    config=AgentConfig(client=client, model=OPUS,
                       model_api_parameters={"max_tokens": 4096}))

async def orchestrate(subtasks: list[WorkerIn]) -> LeaderOut:
    results = await asyncio.gather(*(make_worker().run_async(t) for t in subtasks))
    return await leader.run_async(LeaderIn(parts=[r for r in results]))
```

## Model switching

- Per agent: change the `model=` string on its `AgentConfig` (SONNET ↔ OPUS).
- Anthropic requires `max_tokens` in `model_api_parameters` on every call.
- To swap providers entirely (OpenAI, Gemini, Groq, Ollama) wrap a different Instructor
  client — schemas and hooks are unchanged. See [providers.md](providers.md).

## Rules

- One `ChatHistory` per concurrent agent (or none) — sharing across `asyncio.gather`
  races and corrupts state.
- Cap any supervisor/retry loop the leader runs.
- Keep worker output schemas small and typed; the leader composes them.
