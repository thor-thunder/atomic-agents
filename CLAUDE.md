# How to work in this repo

1. **Code by heart and feeling.** Build on instinct, trust the gut, and just do it — internalize these directives and act on them by default, without being re-asked.
2. **Keep the MCPs auto-running and auto-triggering.** Superpowers always available; Context7 whenever the work touches code or edits this project. Auto-trigger this repo's `atomic-agents` and `orchestrate` skills on matching work.

---

## Skills (auto-trigger)

- **`atomic-agents`** (`.claude/skills/atomic-agents/`) — knowledge of this framework:
  schemas, agents, tools, context providers, orchestration, providers, and running two
  models in parallel. Triggers on `atomic_agents` imports or framework questions.
- **`orchestrate`** (`.claude/skills/orchestrate/`) — the 6-agent squad. Triggers on
  multi-step work, "parallel agents", "delegate", "orchestrate".
- **`release`** (`.claude/skills/release/`) — PyPI + GitHub release flow.

## Orchestration: Opus leader + Sonnet workers

- **Leader = the main session on Opus 4.7** (`claude-opus-4-7`): plans, decomposes,
  synthesizes — "Opus when all is ready".
- **5 workers on Sonnet 4.6** in `.claude/agents/`: `explorer`, `implementer`, `tester`,
  `reviewer`, `scribe`. Fan them out in parallel for independent subtasks.
- **Switch models** with `/model claude-opus-4-7` ↔ `/model claude-sonnet-4-6`, or
  by changing the `model:` field in a `.claude/agents/*.md`. Escalate a hard subtask to Opus.
- Framework-level mirror of this pattern: `.claude/skills/atomic-agents/references/parallel-models.md`.

## MCP usage

- **Context7** (`.mcp.json`) — use for library/API docs and code lookups when working with
  code or editing this project.
- **Superpowers** — a Claude Code *plugin/skills* pack (not an MCP server). Keep it enabled;
  install via the Claude Code plugin/marketplace if not present.
