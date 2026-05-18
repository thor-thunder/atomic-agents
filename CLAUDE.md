## ⚡ Essential Parallel Execution Guidance

**ALWAYS run atomic-agents and the 6-agent team in parallel with MCP running on the side.** This is how the system achieves its full power:

```bash
# Session 1 (Primary): 6-Agent team handles your main request
python -m claude.agents.main --request "Your main task" --verbose

# Session 2 (Parallel): MCP tools discover & integrate available resources
# Tools run asynchronously, discovering capabilities while team works
atomic  # Explore tools, load components

# Session 3 (Parallel): Extended agents handle specialized work
# Custom agents stack on top of team for domain-specific tasks
python custom_agent.py
```

The magic happens when all three run simultaneously — the team orchestrates at the top level while MCP provides dynamic tools and context. See SKILL.md for trigger patterns that activate this automatically.

---

# Atomic Agents Framework - Claude Code Documentation

This is the development documentation for **atomic-agents**, a lightweight and modular Python framework for building Agentic AI applications.

## 📍 Project Overview

**atomic-agents** is a framework built on atomic modularity principles, enabling developers to create AI applications with LEGO-like composability. Every component (agent, tool, schema) is:
- **Single-purpose**: Does one thing well
- **Reusable**: Used in multiple pipelines
- **Composable**: Combines with other components easily
- **Type-safe**: Pydantic-based schemas with full type hints

**Repository:** https://github.com/BrainBlend-AI/atomic-agents

## 🚀 Quick Start

### Installation

```bash
# Core framework
pip install atomic-agents

# Provider SDK (choose one)
pip install instructor[openai]        # For OpenAI
pip install instructor[anthropic]     # For Anthropic
pip install instructor[groq]          # For Groq

# CLI tool
pip install atomic-assembler
atomic --help
```

### 5-Minute Agent Example

```python
from atomic_agents import AtomicAgent, AgentConfig, BasicChatInputSchema, BasicChatOutputSchema
from atomic_agents.context import ChatHistory, SystemPromptGenerator
import instructor
from openai import OpenAI

# Set up client and history
client = instructor.from_openai(OpenAI())
history = ChatHistory()

# Create agent
agent = AtomicAgent[BasicChatInputSchema, BasicChatOutputSchema](
    config=AgentConfig(
        client=client,
        model="gpt-4o-mini",
        history=history,
        system_prompt_generator=SystemPromptGenerator(
            background=["You are a helpful assistant"],
            steps=["Think step by step", "Be concise"],
            output_instructions=["Always provide a clear answer"]
        )
    )
)

# Use agent
response = agent.run(BasicChatInputSchema(chat_message="What is atomic-agents?"))
print(response)
```

---

## 🎯 6-Agent Team System

We provide a **production-ready 6-agent orchestration system** for end-to-end software development:

### The Team

1. **Orchestrator** - Coordinates team, routes tasks, manages workflow
2. **Planner** - Breaks down requirements, designs schemas, defines acceptance criteria
3. **Researcher** - Analyzes requirements, gathers context, identifies constraints
4. **Coder** - Implements code following TDD principles
5. **Reviewer** - Tests code, performs security audit, validates quality
6. **Deployer** - Handles CI/CD, optimization, documentation generation

### Run a Complete Workflow

```bash
cd /home/user/atomic-agents

# Simple workflow
python -m claude.agents.main \
    --request "Add email verification to user signup" \
    --project "my-app" \
    --provider openai \
    --verbose
```

Output includes: planned tasks, research findings, implemented code, test results, security audit, and deployment summary.

### Use the Team Programmatically

```python
from claude.agents.main import AgentTeam

# Create team
team = AgentTeam(provider="openai", verbose=True)

# Run workflow
state = team.run_workflow(
    user_request="Add JWT authentication",
    project_name="auth-service"
)

# Access results
print(f"Tasks: {len(state.planned_tasks)}")
print(f"Code changes: {len(state.code_changes)}")
print(f"Test coverage: {state.test_coverage}%")
print(f"Quality score: {state.code_quality_score}/100")
```

### Full Documentation

→ **See [AGENTS.md](./AGENTS.md)** for complete 6-agent system documentation, workflows, API reference, and best practices.

### 🚀 Running atomic-agents & Team in Parallel

The 6-agent team and atomic-agents framework can work together in parallel for maximum power:

**Parallel Execution Pattern:**
```bash
# Terminal 1: Run the 6-agent team on main tasks
python -m claude.agents.main \
    --request "Build user authentication system" \
    --project "auth-service" \
    --provider openai \
    --verbose

# Terminal 2: Use atomic-agents CLI tool for component tools
atomic  # Interactive tool explorer & downloader

# Terminal 3: Monitor & extend with custom agents
python -c "from claude.agents import AgentTeam; team = AgentTeam()"
```

**Benefits of Parallel Architecture:**
- **Team handles workflow orchestration** (planning, research, implementation, review, deployment)
- **Framework provides core capabilities** (agents, tools, context, schemas)
- **CLI tool (atomic-assembler) manages components** independently
- **Both use same Pydantic/Instructor foundation** for type safety

**Key: They share the same foundation**
```python
# Both team agents and custom agents use:
from atomic_agents import (
    AtomicAgent,           # Base agent class
    BaseIOSchema,          # Schema base
    BaseTool,             # Tool base
)
from atomic_agents.context import (
    SystemPromptGenerator, # Prompt building
    BaseDynamicContextProvider  # Context injection
)
```

---

## 📚 Framework Documentation

### Core Concepts

**AtomicAgent**
- Generic class: `AtomicAgent[InputSchema, OutputSchema]`
- Configuration: `AgentConfig` with client, model, history, prompts
- Methods: `run()`, `run_stream()`, `run_async()`, `run_async_stream()`
- Features: Hooks, context providers, history management, token counting

**Schemas** (BaseIOSchema)
- All inputs/outputs are Pydantic BaseModels
- Docstrings become JSON schema descriptions
- Type safety across the entire pipeline

**Tools** (BaseTool[Input, Output])
- Generic tool class with type-safe I/O
- Used by agents to perform work
- Context: agents can use tools or context providers

**Context Providers** (BaseDynamicContextProvider)
- Inject dynamic context into agent prompts
- Registered on agents and auto-injected
- Used to share state between agents

**System Prompts** (SystemPromptGenerator)
- Builds prompts from sections
- Supports dynamic context injection
- Auto-formats output instructions

### Key Files

| File | Purpose |
|------|---------|
| `/atomic-agents/agents/atomic_agent.py` | Main agent class (~1000 lines) |
| `/atomic-agents/base/base_io_schema.py` | Schema base class |
| `/atomic-agents/base/base_tool.py` | Tool abstraction |
| `/atomic-agents/context/chat_history.py` | Conversation management |
| `/atomic-agents/context/system_prompt_generator.py` | Prompt building |
| `/atomic-agents/connectors/mcp/mcp_factory.py` | MCP tool integration |

### Example Projects

- **Orchestration Agent** - Route between multiple tools
- **Deep Research** - 6-agent research pipeline
- **MCP Agent** - Dynamic tool discovery via Model Context Protocol
- **RAG Chatbot** - Retrieval-augmented generation
- **YouTube Summarizer** - Multi-modal processing

→ **Location:** `/atomic-examples/`

---

## 🔧 Development Workflow

### ⚡ Superpower: Run Everything in Parallel

Harness the full power of atomic-agents by running multiple workflows in parallel:

```bash
# Scenario: Building a complete application stack

# Session 1: Core feature development with the 6-agent team
python -m claude.agents.main \
    --request "Build REST API endpoints" \
    --project "api-server" \
    --verbose

# Session 2: Simultaneously download & integrate atomic tools
atomic  # Browse, download, integrate community tools
# (tool downloader works independently)

# Session 3: Extend with custom specialized agents
python build_custom_agent.py  # Build domain-specific agents
# (agents can be stacked on top of team)

# Result: Orchestrated orchestration!
# The 6-agent team coordinates high-level workflow
# while custom agents handle specialized tasks
# and framework tools power everything underneath
```

**Parallel Superpowers Breakdown:**

| Component | Purpose | Parallelizable |
|-----------|---------|---|
| **6-Agent Team** | Workflow orchestration | Yes - main loop |
| **Framework** | Core capabilities | Yes - reusable |
| **CLI Tools** | Component discovery | Yes - independent |
| **Custom Agents** | Specialized tasks | Yes - tool integration |

### Creating Custom Agents

1. **Define schemas** (inherit from `BaseIOSchema`)
2. **Implement tools** if needed (inherit from `BaseTool`)
3. **Create agent** using `AtomicAgent[Input, Output]`
4. **Configure** system prompt and context providers
5. **Run** and iterate

### Pattern: Tool + Agent

```python
from atomic_agents import BaseIOSchema, BaseTool, AtomicAgent, AgentConfig

# 1. Define schemas
class CalcInput(BaseIOSchema):
    """Calculate something."""
    expression: str

class CalcOutput(BaseIOSchema):
    """Result."""
    result: float
    explanation: str

# 2. Create tool (optional)
class CalcTool(BaseTool[CalcInput, CalcOutput]):
    def run(self, params: CalcInput) -> CalcOutput:
        result = eval(params.expression)
        return CalcOutput(result=result, explanation=f"Evaluated {params.expression}")

# 3. Create agent
agent = AtomicAgent[CalcInput, CalcOutput](
    config=AgentConfig(client=client, model="gpt-4o-mini")
)

# 4. Use
output = agent.run(CalcInput(expression="2 + 2"))
```

### Pattern: State Sharing Between Agents

```python
from atomic_agents.context import BaseDynamicContextProvider

# Create shared state
class SharedState(BaseModel):
    data: List[str]
    metadata: Dict[str, Any]

# Create context provider
class StateProvider(BaseDynamicContextProvider):
    def __init__(self, state: SharedState):
        super().__init__("Shared State")
        self.state = state
    
    def get_info(self) -> str:
        return f"Current data: {json.dumps(self.state.data)}"

# Register on agent
state = SharedState(data=[], metadata={})
agent.register_context_provider("state", StateProvider(state))
```

### Pattern: Tool Result Injection

```python
# Agent 1 generates output
output1 = agent1.run(input1)

# Agent 2 receives Agent 1's results via context
agent2.register_context_provider("prev_result", StateProvider(output1))

# Agent 2 can reference prev_result in its prompt
output2 = agent2.run(input2)
```

---

## 🎓 Learning Resources

### Documentation

- **Main Docs:** https://brainblend-ai.github.io/atomic-agents/
- **API Reference:** https://brainblend-ai.github.io/atomic-agents/api/
- **Examples:** https://github.com/BrainBlend-AI/atomic-agents/tree/main/atomic-examples
- **GitHub Repo:** https://github.com/BrainBlend-AI/atomic-agents

### Related Libraries

- **Instructor:** https://python.useinstructor.com/ - Structured LLM outputs
- **Pydantic:** https://docs.pydantic.dev/ - Data validation and serialization

### Community

- **Discord:** https://discord.gg/J3W9b5AZJR
- **Reddit:** https://www.reddit.com/r/AtomicAgents/
- **GitHub Issues:** https://github.com/BrainBlend-AI/atomic-agents/issues

---

## 💻 Development Setup

### Install for Development

```bash
cd /home/user/atomic-agents

# Using uv (recommended)
uv sync

# OR using pip
pip install -e .
pip install -r requirements.txt
```

### Run Tests

```bash
pytest                          # Run all tests
pytest tests/test_agent.py     # Run specific test
pytest --cov                   # Coverage report
```

### Run Code Quality Checks

```bash
flake8 atomic_agents/
black --check atomic_agents/
mypy atomic_agents/
```

### Build Documentation

```bash
cd docs
make html
open _build/html/index.html
```

---

## 🤖 Using with Claude Code

### CLI Commands

```bash
# Start interactive agent team
python -m claude.agents.main --request "Your task here" --verbose

# Load specific agent
from claude.agents import create_planner_agent

# Import team
from claude.agents import AgentTeam
```

### Project Structure

```
.claude/agents/              # Agent team system
├── shared_state.py         # Shared ProjectState model
├── context_providers.py    # Context injection
├── tools.py               # Safe operations
├── orchestrator.py        # Lead agent
├── planner.py            # Planning agent
├── researcher.py         # Research agent
├── coder.py             # Implementation agent
├── reviewer.py          # Quality agent
├── deployer.py          # Deployment agent
├── main.py             # Orchestration runner
├── config.json         # Team configuration
└── __init__.py        # Module imports

AGENTS.md               # Complete system documentation
```

### Running Workflows

**Feature Development:**
```bash
python -m claude.agents.main \
    --request "Add dark mode toggle" \
    --project "ui-app" \
    --verbose
```

**Bug Fix:**
```bash
python -m claude.agents.main \
    --request "Fix: Images not loading on mobile" \
    --project "mobile-app" \
    --verbose
```

**Security Patch:**
```bash
python -m claude.agents.main \
    --request "Update vulnerable dependency" \
    --project "security-update" \
    --verbose
```

---

## 🔐 Security & Best Practices

### API Key Management

```bash
# Store in .env (never commit!)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Or use environment
export OPENAI_API_KEY="sk-..."
```

### Code Quality Standards

- **Type Safety:** All schemas must have type hints
- **Testing:** Minimum 80% coverage required
- **Security:** All security audit findings must be addressed
- **Documentation:** Auto-generated from code and changes

### Tool Safety

- **ShellExecuteTool:** Whitelist of allowed commands
- **FileOps:** No path traversal, safe permission handling
- **Timeouts:** All operations timeout after specified duration
- **Output Limits:** Prevent token overflow

---

## 📊 Architecture Highlights

### Atomic Modularity

```
Each component is:
✓ Single-purpose
✓ Type-safe (Pydantic)
✓ Composable
✓ Testable
✓ Reusable
```

### Type Safety

```python
# Input/Output are always typed
class MyAgentInput(BaseIOSchema):
    request: str

class MyAgentOutput(BaseIOSchema):
    response: str

# Agent: Input → Process → Output
agent = AtomicAgent[MyAgentInput, MyAgentOutput](...)
output = agent.run(MyAgentInput(request="..."))
# output is MyAgentOutput (type-safe!)
```

### Context Injection

```python
# Dynamic context auto-injected into prompts
agent.register_context_provider("state", StateProvider(state))
agent.register_context_provider("history", HistoryProvider(history))
# Both automatically included in system prompt
```

### Hook System

```python
# Real-time monitoring and interception
agent.register_hook("parse:error", error_handler)
agent.register_hook("completion:response", response_handler)
agent.register_hook("completion:kwargs", kwargs_modifier)
```

---

## 🎯 Next Steps

1. **Read AGENTS.md** - Full 6-agent system documentation
2. **Run a workflow** - Try the agent team on a real task
3. **Study examples** - Review `/atomic-examples/` projects
4. **Build custom agents** - Create agents for your use cases
5. **Join community** - Discord, Reddit, GitHub discussions

---

## 📝 Notes

- Framework uses **Pydantic v2** for schemas
- Built on **Instructor** for structured LLM outputs
- Supports **OpenAI, Anthropic, Groq, Ollama** and more
- **Async/streaming** support built-in
- **Hook system** for custom monitoring/logging
- **MCP support** for dynamic tool discovery

---

## 📄 License

MIT License - See LICENSE file

---

**Last Updated:** 2026-05-18  
**Version:** 2.2.2  
**Status:** Production Ready

For detailed information on the 6-agent team system, see **[AGENTS.md](./AGENTS.md)**.
