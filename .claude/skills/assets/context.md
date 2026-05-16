# Context.md - Atomic Agents Framework Reference

## What is Atomic Agents?

Atomic Agents is a lightweight, modular Python framework for building Agentic AI applications. The framework is built around the principle of **atomicity** - creating single-purpose, reusable, and composable components for AI pipelines.

Think of it like building AI applications with LEGO blocks - each component is:
- **Single-purpose**: Does one thing well
- **Reusable**: Can be used in multiple pipelines
- **Composable**: Easily combines with other components
- **Predictable**: Produces consistent, reliable outputs

## Core Philosophy

- **Predictable AI Behavior**: Controlled, schema-driven agent construction vs. autonomous but unpredictable multi-agent systems
- **Modular Development**: Build AI applications using familiar software engineering principles
- **Type Safety**: Consistent input/output contracts through Pydantic schemas
- **Developer Control**: Full visibility and control over AI behavior with no hidden abstractions

## Anatomy of an Agent

Every Atomic Agent consists of:

1. **System Prompt** - Defines agent behavior and purpose
2. **Input Schema** (Pydantic model) - Validates and structures input
3. **Output Schema** (Pydantic model) - Ensures consistent output format
4. **Chat History** - Maintains conversation context
5. **Context Providers** - Injects dynamic runtime context
6. **Tools** (optional) - Function calling capabilities

## Project Structure

```
atomic-agents/
├── atomic-agents/          # Core framework library (PyPI: atomic-agents)
├── atomic-assembler/       # CLI tool for managing components
├── atomic-examples/        # Example projects and use cases
├── atomic-forge/           # Collection of downloadable tools
├── docs/                   # Sphinx documentation
├── guides/                 # Development guides
└── README.md              # Main documentation
```

### Package Details

**atomic-agents/** (Core Framework)
- `agents/` - AtomicAgent class and agent configuration
- `base/` - Base abstractions (BaseIOSchema, BaseTool, BasePrompt)
- `context/` - Chat history and system prompt generation
- `connectors/` - External integrations (MCP support)
- `memory/` - Memory management systems
- `prompting/` - Prompt engineering utilities
- `services/` - Service integrations

**atomic-assembler/** (CLI Tool)
- Interactive TUI for browsing and downloading tools
- Command: `atomic`

**atomic-forge/** (Tool Repository)
- arxiv_search, bocha_search, calculator, datetime_tool
- fia_signals, hackernews_search, pdf_reader, searxng_search
- tavily_search, weather, webpage_scraper, wikipedia_search, youtube_transcript_scraper

## Core Technologies

- **Language**: Python 3.12+
- **AI/LLM Integration**: Instructor (supports 10+ providers)
- **Data Validation**: Pydantic v2
- **CLI Framework**: Textual (TUI), Rich (terminal formatting)
- **Testing**: pytest with coverage
- **Documentation**: Sphinx + MyST + ReadTheDocs
- **Build System**: uv (with hatchling)

## LLM Provider Compatibility

Through Instructor, supports all major providers:
- OpenAI, Anthropic (Claude), Groq, Mistral, Cohere, Google Gemini, Ollama, and more

## Execution Modes

- **Synchronous**: `agent.run(input_data)`
- **Asynchronous**: `await agent.run_async(input_data)`
- **Streaming**: `agent.run_stream(input_data)` and `agent.run_async_stream(input_data)`

## 6-Layer Agent Hierarchy (Atomic Agents Pattern)

For complex workflows, use a 6-layer hierarchy:

1. **Researcher** (Sub-Agent-1): Investigates requirements and gathers information
2. **Planner** (Sub-Agent-2): Designs approach and breaks down tasks
3. **Architect** (Sub-Agent-3): Structures solution and defines interfaces
4. **Builder** (Sub-Agent-4): Implements code and creates components
5. **Critic/Refiner** (Sub-Agent-5): Reviews, tests, and improves work
6. **Supreme Leader Orchestrator** (Main Agent): Coordinates all sub-agents and manages workflow

### Model Assignment for 6-Layer Pattern
- **Opus-4.6**: Supreme Leader Orchestrator (reasoning, coordination, complex analysis)
- **Haiku-4.5**: All sub-agents (efficiency, parallel execution, cost optimization)

## Key Design Patterns

### 1. Single Responsibility Principle
Each component does one thing well. Agents, tools, and schemas are atomic units of functionality.

### 2. Type-Safe Contracts
Pydantic schemas enforce contracts at runtime, catching errors before they propagate.

### 3. Composition Over Inheritance
Build complex behaviors by composing simple agents rather than deep inheritance hierarchies.

### 4. Schema-Driven Development
All data flows through typed Pydantic schemas.

### 5. Composability Pattern
Agents can be chained by connecting output schemas to input schemas:
```
Agent A (OutputSchemaA) → Agent B (InputSchemaB) → Agent C (OutputSchemaC)
```

### 6. Context Providers
Dynamic context injection allows runtime enhancement of prompts without modifying agent code.

### 7. Separation of Concerns
- **Prompts** define behavior
- **Schemas** define data contracts
- **Tools** define capabilities
- **Context Providers** inject runtime information

## Development Tools & Commands

```bash
# Installation
pip install atomic-agents
uv sync  # For development

# Code quality
uv run black atomic-agents atomic-assembler atomic-examples atomic-forge
uv run flake8 --extend-exclude=.venv atomic-agents atomic-assembler atomic-examples atomic-forge
uv run pytest --cov=atomic_agents atomic-agents

# Documentation
cd docs && make html
```

## Version 2.0+ Improvements

- Cleaner imports (removed `.lib` from import paths)
- Renamed classes (`BaseAgent` → `AtomicAgent`, `BaseAgentConfig` → `AgentConfig`)
- Better type safety with generic type parameters
- Enhanced streaming capabilities
- Improved module organization

## Resources

- **Main Docs**: https://brainblend-ai.github.io/atomic-agents/
- **Repository**: https://github.com/BrainBlend-AI/atomic-agents
- **PyPI**: https://pypi.org/project/atomic-agents/
- **Discord**: https://discord.gg/J3W9b5AZJR
- **Subreddit**: /r/AtomicAgents
