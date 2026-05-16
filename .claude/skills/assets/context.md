# Context.md - Shared Language for Atomic Agents

This file establishes a shared language to prevent context drift and verbosity cascades across the codebase.

## Core Concepts

### Atomicity
Each component (agent, tool, context provider) is:
- **Single-purpose**: Does one thing well
- **Reusable**: Can be used in multiple pipelines
- **Composable**: Easily combines with other components
- **Predictable**: Produces consistent, reliable outputs

### Agent Architecture
- **Agent**: Autonomous unit executing defined tasks
- **Tool**: Reusable function agents can call
- **Context Provider**: Supplies relevant context during execution
- **Schema**: Pydantic-based structured outputs

### Agent Hierarchy (6-Layer)
1. **Researcher** (Sub-Agent-1): Investigates requirements
2. **Planner** (Sub-Agent-2): Designs approach
3. **Architect** (Sub-Agent-3): Structures solution
4. **Builder** (Sub-Agent-4): Implements code
5. **Critic/Refiner** (Sub-Agent-5): Reviews and improves
6. **Supreme Leader Orchestrator** (Main Agent): Coordinates all sub-agents

### Model Assignment
- **Opus-4.6**: Supreme Leader Orchestrator (reasoning, coordination)
- **Haiku-4.5**: All sub-agents (efficiency, parallel execution)

## Anchoring Rules

1. **Single Source of Truth**: Return to this file before adding new concepts
2. **No Context Drift**: When discussing design decisions, reference this shared language
3. **Minimal Abstractions**: Only create new terminology when it solves a real verbosity problem
4. **Decision Tree Clarity**: Every decision branches from a parent concept defined here
