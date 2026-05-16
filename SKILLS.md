# Skills - Atomic Agents Development Framework

## What is Atomic Agents?

Atomic Agents is a lightweight, modular Python framework for building Agentic AI applications. The framework is built around the principle of **atomicity** - creating single-purpose, reusable, and composable components for AI pipelines.

Think of it like building AI applications with LEGO blocks - each component is:
- **Single-purpose**: Does one thing well
- **Reusable**: Can be used in multiple pipelines
- **Composable**: Easily combines with other components
- **Predictable**: Produces consistent, reliable outputs

## Tool Calling & UI Generation Workflow

* **Always**: Describe scene → Claude generates SVG/Canvas/React component → Replit previews live

This pattern enables rapid prototyping and visualization of agent outputs through integrated tool calling.

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
