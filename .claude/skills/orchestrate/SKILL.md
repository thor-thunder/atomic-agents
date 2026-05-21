---
name: orchestrate
description: Coordinate the 6-agent squad — an Opus 4.7 leader plus five Sonnet 4.6 workers (explorer, implementer, tester, reviewer, scribe). Auto-triggers when the user asks to "orchestrate", run "agents in parallel", "delegate", "use the squad", or tackles a multi-step task big enough to split into independent subtasks. Documents how to fan out to Sonnet workers and switch models.
---

# Orchestrate — Opus leader + Sonnet workers

A 6-agent squad for multi-step work. The **leader** (Opus 4.7) plans and synthesizes; the
five **workers** (Sonnet 4.6) do scoped subtasks in parallel. Worker definitions live in
`.claude/agents/`.

| Role | Agent | Model | Use for |
|---|---|---|---|
| Leader | (main session) / `orchestrator` | Opus 4.7 | Plan, decompose, synthesize, hard reasoning |
| Research | `explorer` | Sonnet 4.6 | Read-only search, mapping a feature |
| Build | `implementer` | Sonnet 4.6 | Write/edit code from a spec |
| Verify | `tester` | Sonnet 4.6 | Run/write tests |
| Review | `reviewer` | Sonnet 4.6 | Read-only code review |
| Document | `scribe` | Sonnet 4.6 | Docs, summaries, condensing |

## How it runs

1. **Leader plans (Opus).** The main Opus 4.7 session restates the goal and splits it into
   the smallest independent subtasks. The leader is the main thread — subagents can't spawn
   their own subagents, so keep the planning/synthesis here.
2. **Fan out to workers (Sonnet).** Launch independent subtasks concurrently via the Agent
   tool — **one message, multiple Agent calls** (`subagent_type` = `explorer`, `implementer`,
   `tester`, `reviewer`, `scribe`). Each gets enough self-contained context to act.
3. **Sequence only when needed.** Use a sequential step when one worker's output feeds the next.
4. **Synthesize (Opus).** When workers return, the leader integrates results, resolves
   conflicts, and produces the final answer — "Opus is best when all is ready".

## Switching models

- **Session leader:** `/model claude-opus-4-7` for the leader; `/model claude-sonnet-4-6`
  to run the whole session at the worker tier.
- **Per worker:** each `.claude/agents/*.md` sets `model:` (`sonnet` for workers, `opus` for
  `orchestrator`). Change that field to re-tier an agent (e.g. `haiku` for cheap fan-out).
- **Escalate a subtask:** if a worker subtask needs hard reasoning, the leader does it on
  Opus instead of forcing a Sonnet worker through it.

## When to use

- Multi-file features, broad research, or anything that splits into independent parts → fan out.
- A single small edit or a quick question → just do it in the main thread; the squad's
  isolation overhead isn't worth it.

This pattern mirrors the framework-level two-model setup in the `atomic-agents` skill —
see `.claude/skills/atomic-agents/references/parallel-models.md`.
