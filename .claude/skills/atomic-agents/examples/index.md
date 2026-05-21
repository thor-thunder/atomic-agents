# Runnable Examples (in this repo)

Pointers into `atomic-examples/` — read these for full, working code rather than copying
snippets.

| Example | Path | Shows |
|---|---|---|
| Quickstart | `atomic-examples/quickstart/quickstart/1_0_basic_chatbot.py` | Minimal agent |
| Streaming | `atomic-examples/quickstart/quickstart/1_1_basic_chatbot_streaming.py` | `run_stream` |
| Custom schema | `atomic-examples/quickstart/quickstart/3_0_basic_custom_chatbot_with_custom_schema.py` | Typed I/O |
| Multi-provider | `atomic-examples/quickstart/quickstart/4_basic_chatbot_different_providers.py` | Swap providers/models |
| Orchestration / router | `atomic-examples/orchestration-agent/` | Typed tool routing |
| Deep research | `atomic-examples/deep-research/` | Sequential pipeline |
| Progressive disclosure | `atomic-examples/progressive-disclosure/` | Search + execute over many tools |
| Hooks | `atomic-examples/hooks-example/hooks_example/main.py` | Telemetry, retries |
| MCP | `atomic-examples/mcp-agent/` | MCP client + server |
| RAG chatbot | `atomic-examples/rag-chatbot/` | Context-provider RAG |

For the leader+workers / two-model pattern at the framework level, see
[../references/parallel-models.md](../references/parallel-models.md).
