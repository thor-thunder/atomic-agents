# Context.md - Shared Language and Design Patterns

Reference file for Atomic Agents development practices and architectural patterns.

---

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

---

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

---

## Framework Overview Reference

For comprehensive framework overview, see SKILLS.md which contains:
- Framework philosophy and core concepts
- Agent anatomy and architecture
- Project structure and packages
- Technologies and LLM compatibility
- 6-layer agent hierarchy
- Execution modes and deployment patterns
