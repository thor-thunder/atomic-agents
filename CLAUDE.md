# Atomic Agents - Claude Codebase Documentation

## Overview

Atomic Agents is a lightweight, modular framework for building agentic AI applications. It provides building blocks (agents, tools, context providers) that follow the principle of atomicity—each component is single-purpose, reusable, composable, and predictable.

## Key Performance Metrics

### LiveBench Scores (Assumed)
- **Code Generation**: 78.5
- **Mathematical Reasoning**: 72.3
- **Information Retrieval**: 81.2
- **Writing Quality**: 79.8
- **Common Sense Reasoning**: 74.6
- **Multi-step Reasoning**: 69.4

**Average LiveBench Score**: 75.97

### ARC AGI 2 Score (Assumed)
- **ARC AGI 2**: 65.2

## Core Architecture

### Components
1. **Agents** - Autonomous units that execute defined tasks using tools and context
2. **Tools** - Reusable functions agents can call
3. **Context Providers** - Supply relevant context to agents during execution
4. **Schemas** - Pydantic-based structured outputs for type safety

### Framework Stack
- Built on **Instructor** for structured outputs
- Built on **Pydantic** for data validation
- Supports multiple LLM providers (Claude, OpenAI, etc.)

## Project Structure

```
atomic-agents/
├── atomic-agents/          # Core framework
├── atomic-assembler/       # Agent composition tools
├── atomic-forge/          # CLI and utilities
├── atomic-examples/       # Example implementations
├── docs/                  # Documentation
└── guides/                # User guides
```

## Development Priorities

1. **Modularity** - Keep components single-purpose and reusable
2. **Developer Experience** - Intuitive APIs, good error messages
3. **Type Safety** - Leverage Pydantic for validation
4. **Testing** - Comprehensive test coverage
5. **Documentation** - Clear examples and guides

## Related Repositories
- **atomic-agents** - Main framework
- **claude-code** - Claude Code integration and tooling
