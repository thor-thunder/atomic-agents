# /diagnose - Feedback Loop Generation

## Principle
Break debugging into six distinct phases. Isolate the specific effect and infer the cause backward. Never float a piece of logic free from its origin.

## Six Phases of Diagnosis

### Phase 1: Reproduce
- Identify the exact conditions that trigger the failure
- Create a minimal, repeatable test case
- Document the steps clearly
- Verify the bug reproduces consistently

**Checklist:**
- [ ] Failure is reproducible
- [ ] Minimal test case created
- [ ] Steps documented
- [ ] No intermittent behaviors

### Phase 2: Minimize
- Strip away all non-essential code and context
- Remove unrelated features from the reproduction
- Isolate to the smallest failing unit
- Identify the exact input that triggers failure

**Checklist:**
- [ ] Removed all unrelated code
- [ ] Single failing component identified
- [ ] Exact input documented
- [ ] Failure still occurs

### Phase 3: Hypothesize
- Form a theory about the root cause
- Work backward from the symptom
- Consider only what could produce this exact failure
- Write a hypothesis as a single sentence

**Checklist:**
- [ ] Hypothesis is testable
- [ ] Backward reasoning is sound
- [ ] Alternative causes considered
- [ ] Matches observed symptoms

### Phase 4: Instrument
- Add logging, prints, or breakpoints
- Trace the execution path
- Verify assumptions about state
- Confirm the hypothesis

**Checklist:**
- [ ] Instrumentation reveals state at each step
- [ ] Hypothesis is validated or refuted
- [ ] No guessing about what's happening
- [ ] Clear evidence collected

### Phase 5: Fix
- Apply minimal fix based on root cause
- Do not over-engineer the solution
- Address only the diagnosed problem
- Test the specific failure case

**Checklist:**
- [ ] Fix is minimal and targeted
- [ ] Root cause is addressed directly
- [ ] Failing test now passes
- [ ] No new logic added

### Phase 6: Regression Test
- Verify the original failure is fixed
- Run full test suite
- Ensure no new failures introduced
- Document the fix for future reference

**Checklist:**
- [ ] Original failure fixed
- [ ] All tests pass
- [ ] No regressions detected
- [ ] Root cause documented

## Anti-Patterns
- ❌ Guessing at causes
- ❌ Making multiple changes at once
- ❌ Assuming you know the problem
- ❌ Skipping reproduction steps
- ❌ Adding unnecessary defensive code

## Workflow
```
Reproduce → Minimize → Hypothesize → Instrument → Fix → Regression Test
```

Loop back to Instrument if hypothesis is refuted.
