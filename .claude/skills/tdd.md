# /tdd - Vertical Slicing Development

## Principle
Break development into strict, isolated vertical slices. Never write tests or code in bulk. One test → one implementation → one green bar.

## Workflow

### Step 1: Write One Failing Test
- Write a single, specific test for one behavior
- Run it; verify it fails
- Make the test as small as possible
- Focus on one assertion at a time

### Step 2: Implement Minimal Code
- Write only enough code to make that one test pass
- Do not write "future-proofing" code
- Do not add error handling unless the test requires it
- Keep the implementation as simple as possible

### Step 3: Green Bar
- Run the test suite
- Verify only your test passes
- No regressions in other tests

### Step 4: Refactor (Optional)
- Only after green, improve code quality
- Do not change behavior
- Do not add new features
- Keep tests green throughout

## Anti-Patterns
- ❌ Writing multiple tests before implementing
- ❌ Bulk implementation across multiple features
- ❌ Adding "nice-to-have" error handling
- ❌ Pre-optimizing code
- ❌ Skipping tests to move faster

## Checklist
- [ ] Test is specific and isolated
- [ ] Test fails for the right reason
- [ ] Implementation is minimal
- [ ] All tests pass
- [ ] No regressions introduced
