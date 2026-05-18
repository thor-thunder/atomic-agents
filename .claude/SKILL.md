---
name: agents
description: Run the 6-agent atomic orchestration team. Automatically triggered when user asks to "build", "implement", "develop", "create", "fix", "refactor", "add feature", "deploy", or describes a software development task. Full documentation in AGENTS.md.
allowed-tools: Bash, Read, Write
triggers:
  - "build [feature/app]"
  - "implement [feature]"
  - "develop [feature]"
  - "create [component]"
  - "fix [bug]"
  - "refactor [code]"
  - "add [feature]"
  - "deploy [code]"
  - "write [code/tests]"
  - "optimize [performance]"
  - "document [feature]"
  - "[workflow/task] from start to finish"
  - "handle [requirement]"
  - "setup [system]"
---

# Atomic Agents 6-Team System - SKILL.md

Professional orchestration system that automatically activates when you need software development work done.

## Automatic Trigger Phrases

The agent team activates when you use any of these patterns:

### Feature Development
- "Build a [feature]"
- "Implement [feature] with tests"
- "Develop [component]"
- "Add [capability] to the system"
- "Create a new [feature]"

### Bug Fixes & Refactoring
- "Fix the [bug] where..."
- "Refactor [code/module]"
- "Optimize [performance] in..."
- "Clean up [code]"

### Deployment & Operations
- "Deploy [feature] to production"
- "Release [version]"
- "Setup [environment/service]"
- "Migrate to [platform]"

### Documentation & Analysis
- "Document [feature/API]"
- "Analyze [requirement/problem]"
- "Review [code/design]"
- "Document the [workflow]"

## Quick Start

### Trigger the Agents

Simply describe what you need built:

```
Build a user authentication system with JWT tokens
```

This automatically routes to the 6-agent team:
1. **Orchestrator** determines the workflow
2. **Planner** breaks it into tasks
3. **Researcher** gathers context
4. **Coder** implements with TDD
5. **Reviewer** validates quality & security
6. **Deployer** handles CI/CD & documentation

### Monitor Progress

Use the `--verbose` flag to see each agent's work:

```bash
python -m claude.agents.main \
    --request "Your request here" \
    --project "project-name" \
    --verbose
```

Output includes:
- Tasks planned
- Research findings
- Code changes
- Test results
- Security audit
- Deployment status

### Access Results

The agent team returns a `ProjectState` with everything:

```python
from claude.agents.main import AgentTeam

team = AgentTeam(verbose=True)
state = team.run_workflow(
    user_request="Build feature X",
    project_name="my-app"
)

# Access all results
print(f"Tasks: {len(state.planned_tasks)}")
print(f"Code files: {len(state.code_changes)}")
print(f"Coverage: {state.test_coverage}%")
print(f"Security issues: {len(state.security_audit_findings)}")
print(f"Status: {state.deployment_status}")
```

## Workflow Stages

The agents coordinate through these stages automatically:

```
User Request
    ↓
planning        → [Planner] breaks into tasks
    ↓
research        → [Researcher] gathers context
    ↓
implementation  → [Coder] writes TDD code
    ↓
review          → [Reviewer] validates quality/security
    ↓
deployment      → [Deployer] handles CI/CD & docs
    ↓
Results + State
```

## Key Superpowers

### 1. Automatic Task Breakdown
Planner automatically creates tasks with acceptance criteria from your request.

### 2. TDD-First Implementation
Coder writes tests BEFORE code, ensuring quality.

### 3. Security & Quality Gates
Reviewer validates:
- Test coverage ≥80%
- No critical security issues
- All acceptance criteria met
- Code quality ≥75/100

### 4. Documentation Generation
Deployer auto-generates:
- API documentation
- Implementation guides
- Deployment notes
- Release changelog

### 5. Shared State Flow
All agents contribute to ProjectState:
```python
state.planned_tasks        # From Planner
state.research_findings    # From Researcher
state.code_changes         # From Coder
state.test_results         # From Reviewer
state.deployment_steps     # From Deployer
```

## Multi-Provider Support

Choose your LLM provider:

```bash
# OpenAI (default, fastest)
--provider openai --model gpt-4o-mini

# Anthropic (most capable thinking)
--provider anthropic --model claude-3-5-sonnet

# Groq (ultra-fast)
--provider groq --model mixtral-8x7b-32768
```

## Parallel Execution Superpowers

Run multiple agent teams in parallel for maximum throughput:

```bash
# Terminal 1: Main feature development
python -m claude.agents.main --request "Build API" --verbose

# Terminal 2: Concurrent documentation
python -m claude.agents.main --request "Document API" --verbose

# Terminal 3: Security-focused review
python -m claude.agents.main --request "Security audit" --verbose
```

All teams use shared ProjectState, tools, and framework → orchestrated coordination!

## When to Use This System

✓ Building new features end-to-end  
✓ Fixing bugs with comprehensive testing  
✓ Refactoring with quality validation  
✓ Creating production-ready code  
✓ Deploying with confidence  
✓ Auto-generating documentation  
✓ Security-critical features  
✓ Performance optimization  

## Full Documentation

For complete specifications, agent details, API reference, and examples:

→ **See [AGENTS.md](./AGENTS.md)**

This SKILL.md provides quick triggers and overview. AGENTS.md has full system documentation.

## Example Workflows

### New Feature (End-to-End)

```
User: "Build a caching layer for database queries"

System automatically:
1. [Planner] Creates 4 tasks with acceptance criteria
2. [Researcher] Analyzes caching strategies & constraints
3. [Coder] Writes cache implementation + tests (TDD)
4. [Reviewer] Validates coverage, performance, security
5. [Deployer] Deploys to staging, measures latency improvement
6. Returns: Complete working feature + docs
```

### Bug Fix (Fast Track)

```
User: "Fix: User images not loading on mobile"

System automatically:
1. [Planner] Task: Fix mobile image loading
2. [Researcher] Reviews responsive design best practices
3. [Coder] Implements fix + mobile-specific tests
4. [Reviewer] Validates on multiple devices, no regressions
5. [Deployer] Deploys fix, monitors image load metrics
6. Returns: Fixed bug + regression tests + monitoring
```

### Security Update (Priority)

```
User: "Update vulnerable dependency + test thoroughly"

System automatically:
1. [Planner] Create update + compatibility verification tasks
2. [Researcher] Analyze migration guide, breaking changes
3. [Coder] Update dependencies, test for breaks
4. [Reviewer] Run full test suite, security audit
5. [Deployer] Deploy to staging first, then production
6. Returns: Secure update + full test suite + safety checks
```

## Integration with atomic-agents

This skill works seamlessly with the atomic-agents framework:

- **Type Safety**: All schemas use Pydantic
- **Composability**: Each agent is reusable
- **Context Injection**: Shared state flows through prompts
- **Tool Integration**: Agents use framework tools
- **Multi-Provider**: Works with any Instructor-supported LLM

The 6-agent team IS atomic-agents in action!

## Notes

- Automatically handles errors and retries
- Provides detailed state tracking
- Generates comprehensive audit logs
- Supports dry-run mode (preview without executing)
- Thread-safe for parallel execution
- Production-grade security and validation

**Status:** Ready for production use  
**Last Updated:** 2026-05-18  
**Documentation:** [AGENTS.md](./AGENTS.md)
