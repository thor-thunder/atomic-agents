# Skills - Atomic Agents Development Framework

This document outlines the disciplined, minimalist reasoning framework for atomic-agents development. Based on Matt Pocock's skills-driven approach, these skills enforce structural soundness and prevent context drift.

---

## context.md - Shared Language for Atomic Agents

This file establishes a shared language to prevent context drift and verbosity cascades across the codebase.

### Core Concepts

#### Atomicity
Each component (agent, tool, context provider) is:
- **Single-purpose**: Does one thing well
- **Reusable**: Can be used in multiple pipelines
- **Composable**: Easily combines with other components
- **Predictable**: Produces consistent, reliable outputs

#### Agent Architecture
- **Agent**: Autonomous unit executing defined tasks
- **Tool**: Reusable function agents can call
- **Context Provider**: Supplies relevant context during execution
- **Schema**: Pydantic-based structured outputs

#### Agent Hierarchy (6-Layer)
1. **Researcher** (Sub-Agent-1): Investigates requirements
2. **Planner** (Sub-Agent-2): Designs approach
3. **Architect** (Sub-Agent-3): Structures solution
4. **Builder** (Sub-Agent-4): Implements code
5. **Critic/Refiner** (Sub-Agent-5): Reviews and improves
6. **Supreme Leader Orchestrator** (Main Agent): Coordinates all sub-agents

#### Model Assignment
- **Opus-4.6**: Supreme Leader Orchestrator (reasoning, coordination)
- **Haiku-4.5**: All sub-agents (efficiency, parallel execution)

### Anchoring Rules

1. **Single Source of Truth**: Return to this section before adding new concepts
2. **No Context Drift**: When discussing design decisions, reference this shared language
3. **Minimal Abstractions**: Only create new terminology when it solves a real verbosity problem
4. **Decision Tree Clarity**: Every decision branches from a parent concept defined here

---

## /tdd - Vertical Slicing Development

Break development into strict, isolated vertical slices. Never write tests or code in bulk. One test → one implementation → one green bar.

### Workflow

#### Step 1: Write One Failing Test
- Write a single, specific test for one behavior
- Run it; verify it fails
- Make the test as small as possible
- Focus on one assertion at a time

#### Step 2: Implement Minimal Code
- Write only enough code to make that one test pass
- Do not write "future-proofing" code
- Do not add error handling unless the test requires it
- Keep the implementation as simple as possible

#### Step 3: Green Bar
- Run the test suite
- Verify only your test passes
- No regressions in other tests

#### Step 4: Refactor (Optional)
- Only after green, improve code quality
- Do not change behavior
- Do not add new features
- Keep tests green throughout

### Anti-Patterns
- ❌ Writing multiple tests before implementing
- ❌ Bulk implementation across multiple features
- ❌ Adding "nice-to-have" error handling
- ❌ Pre-optimizing code
- ❌ Skipping tests to move faster

### Checklist
- [ ] Test is specific and isolated
- [ ] Test fails for the right reason
- [ ] Implementation is minimal
- [ ] All tests pass
- [ ] No regressions introduced

---

## /diagnose - Feedback Loop Generation

Break debugging into six distinct phases. Isolate the specific effect and infer the cause backward. Never float a piece of logic free from its origin.

### Six Phases of Diagnosis

#### Phase 1: Reproduce
- Identify the exact conditions that trigger the failure
- Create a minimal, repeatable test case
- Document the steps clearly
- Verify the bug reproduces consistently

**Checklist:**
- [ ] Failure is reproducible
- [ ] Minimal test case created
- [ ] Steps documented
- [ ] No intermittent behaviors

#### Phase 2: Minimize
- Strip away all non-essential code and context
- Remove unrelated features from the reproduction
- Isolate to the smallest failing unit
- Identify the exact input that triggers failure

**Checklist:**
- [ ] Removed all unrelated code
- [ ] Single failing component identified
- [ ] Exact input documented
- [ ] Failure still occurs

#### Phase 3: Hypothesize
- Form a theory about the root cause
- Work backward from the symptom
- Consider only what could produce this exact failure
- Write a hypothesis as a single sentence

**Checklist:**
- [ ] Hypothesis is testable
- [ ] Backward reasoning is sound
- [ ] Alternative causes considered
- [ ] Matches observed symptoms

#### Phase 4: Instrument
- Add logging, prints, or breakpoints
- Trace the execution path
- Verify assumptions about state
- Confirm the hypothesis

**Checklist:**
- [ ] Instrumentation reveals state at each step
- [ ] Hypothesis is validated or refuted
- [ ] No guessing about what's happening
- [ ] Clear evidence collected

#### Phase 5: Fix
- Apply minimal fix based on root cause
- Do not over-engineer the solution
- Address only the diagnosed problem
- Test the specific failure case

**Checklist:**
- [ ] Fix is minimal and targeted
- [ ] Root cause is addressed directly
- [ ] Failing test now passes
- [ ] No new logic added

#### Phase 6: Regression Test
- Verify the original failure is fixed
- Run full test suite
- Ensure no new failures introduced
- Document the fix for future reference

**Checklist:**
- [ ] Original failure fixed
- [ ] All tests pass
- [ ] No regressions detected
- [ ] Root cause documented

### Anti-Patterns
- ❌ Guessing at causes
- ❌ Making multiple changes at once
- ❌ Assuming you know the problem
- ❌ Skipping reproduction steps
- ❌ Adding unnecessary defensive code

### Workflow
```
Reproduce → Minimize → Hypothesize → Instrument → Fix → Regression Test
```

Loop back to Instrument if hypothesis is refuted.

---

## Philosophy

- **Let AI build it, and iterate by feeling**: Trust the process and refine based on results
- **No years of technical training required**: These frameworks make sophisticated development accessible
- **Relentless clarity**: Interview every aspect of the plan until reaching shared understanding
- **Walk the design tree**: Resolve dependencies between decisions one by one, branch by branch
