# Atomic Agents 6-Team System

Professional orchestration system implementing a 6-agent team that collaboratively handles end-to-end software development tasks using the atomic-agents framework.

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Team Overview](#team-overview)
3. [Architecture](#architecture)
4. [Shared State Model](#shared-state-model)
5. [Agent Specifications](#agent-specifications)
6. [Communication Protocols](#communication-protocols)
7. [Execution Workflows](#execution-workflows)
8. [Installation & Setup](#installation--setup)
9. [Usage Examples](#usage-examples)
10. [API Reference](#api-reference)
11. [Best Practices](#best-practices)

---

## Executive Summary

This system implements a modular, type-safe 6-agent team that coordinates to handle complex development tasks. Each agent has a specific role in the workflow:

1. **Orchestrator** - Coordinates the team and manages workflow
2. **Planner** - Breaks down requirements into tasks with acceptance criteria
3. **Researcher** - Analyzes requirements and gathers context
4. **Coder** - Implements code following TDD principles
5. **Reviewer** - Tests code, performs security audit, validates quality
6. **Deployer** - Handles CI/CD, optimization, and documentation

**Key Characteristics:**
- **Atomic Modularity**: Each agent is type-safe with clear Input/Output schemas
- **Shared State**: All agents read/write to a unified ProjectState model
- **Context Injection**: Agents receive relevant context via context providers
- **Hand-Off Protocol**: Clear protocol for agent-to-agent coordination
- **Production-Ready**: Follows security best practices, includes validation, error handling

### Use Cases

- **Feature Development**: From request to deployment
- **Bug Fixes**: Analysis → Fix → Test → Deploy
- **Refactoring**: Plan → Implement → Review → Deploy
- **Documentation**: Auto-generate from code and changes
- **Security Updates**: Quick-turnaround security patches

---

## Team Overview

### The 6 Agents

```
User Request
    ↓
[Orchestrator] ←→ Coordinates Workflow ←→ Updates ProjectState
    ↓
[Planner] → Breaks into Tasks & Schemas
    ↓
[Researcher] → Gathers Context & Constraints
    ↓
[Coder] → Implements with TDD Tests
    ↓
[Reviewer] → Tests, Security, Quality Validation
    ↓
[Deployer] → CI/CD, Performance, Documentation
    ↓
Deployed Feature + Docs
```

### Agent Capabilities Matrix

| Agent | Input | Output | Tools | Context |
|-------|-------|--------|-------|---------|
| **Orchestrator** | User request, State | Next agent, Instruction | State routing | Full state |
| **Planner** | Request, State | Tasks, Schemas | None | Project state |
| **Researcher** | Topic, State | Findings, Constraints | File reader | Task context |
| **Coder** | Task, State, Schemas | Code, Tests | File I/O, Shell | Research, Task |
| **Reviewer** | Code, State | Test results, Quality | Shell (test), Analysis | Code, Review |
| **Deployer** | Code, State | Deployment steps, Docs | Shell, File I/O | Review, Code |

---

## Architecture

### Component Model

```python
ProjectState (Pydantic BaseModel)
    ├── Project metadata
    ├── Planned tasks (Planner output)
    ├── Research findings (Researcher output)
    ├── Code changes (Coder output)
    ├── Test results (Reviewer output)
    ├── Deployment status (Deployer output)
    └── Workflow tracking

Agents (AtomicAgent[Input, Output])
    ├── Input: Typed Pydantic schema
    ├── Output: Typed Pydantic schema
    ├── Tools: Safe file/shell operations
    ├── Context Providers: State injection
    └── System Prompt: Role definition

Context Providers (BaseDynamicContextProvider)
    ├── ProjectStateContextProvider
    ├── TaskContextProvider
    ├── ResearchContextProvider
    ├── CodeContextProvider
    └── ReviewContextProvider

Tools (BaseTool[Input, Output])
    ├── FileReadTool
    ├── FileWriteTool
    ├── DirectoryListTool
    ├── ShellExecuteTool
    └── CodeAnalysisTool
```

### Execution Flow

```
1. User submits request to Orchestrator
   ↓
2. Orchestrator determines next stage (planning → research → implementation → review → deployment)
   ↓
3. Route to appropriate agent (Planner, Researcher, Coder, Reviewer, or Deployer)
   ↓
4. Agent reads ProjectState from context providers
   ↓
5. Agent processes: reads inputs, uses tools, generates outputs
   ↓
6. Agent updates ProjectState with results
   ↓
7. If workflow complete, done. Otherwise, back to step 2
```

---

## Shared State Model

The `ProjectState` is a Pydantic BaseModel that all agents can read and write to. It contains:

### Basic Project Info

```python
class ProjectState(BaseModel):
    project_name: str              # Project identifier
    project_description: str       # What is this project?
    user_request: str             # Original user request
```

### Planner Outputs

```python
    planned_tasks: List[PlannedTask]  # Tasks with acceptance criteria
    # Each PlannedTask contains:
    #   - task_id, title, description
    #   - acceptance_criteria (verifiable criteria)
    #   - estimated_effort, dependencies
    #   - schema_definitions, assigned_to, status
```

### Researcher Outputs

```python
    research_findings: List[ResearchFindings]  # Analyzed findings
    # Each ResearchFindings contains:
    #   - topic, findings, sources
    #   - constraints, recommendations, context
```

### Coder Outputs

```python
    code_changes: List[CodeChange]  # Files changed/created
    # Each CodeChange contains:
    #   - file_path, change_type (create/modify/delete)
    #   - original_content, new_content
    #   - description, tdd_test_first
    #   - tests_added
    implementation_status: TaskStatus  # PENDING → IN_PROGRESS → COMPLETED
```

### Reviewer Outputs

```python
    test_results: List[TestResult]  # Test execution results
    test_coverage: float            # Code coverage percentage
    security_audit_findings: List[SecurityAuditFinding]  # Vulnerabilities
    code_quality_score: float       # 0-100 quality score
    review_status: TaskStatus       # COMPLETED or BLOCKED
```

### Deployer Outputs

```python
    deployment_steps: List[DeploymentStep]  # Deployment steps executed
    deployment_status: TaskStatus           # COMPLETED or FAILED
    performance_metrics: Dict[str, float]   # Perf metrics
    generated_documentation: Dict[str, str] # Generated docs
    deployed_at: datetime                   # Deployment timestamp
```

### Workflow Tracking

```python
    current_agent: str          # Currently active agent
    workflow_stage: str         # planning → research → implementation → review → deployment
    errors: List[str]           # Errors encountered
    warnings: List[str]         # Warnings
    created_at: datetime
    updated_at: datetime
```

---

## Agent Specifications

### 1. Orchestrator Agent

**Role:** Lead coordinator - routes tasks, manages workflow, tracks progress

**Input Schema: `OrchestratorInput`**
```python
class OrchestratorInput(BaseIOSchema):
    """Input to orchestrator agent."""
    user_request: str                    # User's request
    current_state: ProjectState          # Current project state
    force_stage: Optional[str] = None    # Force specific stage
```

**Output Schema: `OrchestratorOutput`**
```python
class OrchestratorOutput(BaseIOSchema):
    """Output from orchestrator agent."""
    next_agent: str              # Which agent executes next
    instruction: str             # Clear task instruction
    reasoning: str               # Why this choice
    workflow_complete: bool      # Is workflow done?
    state_updates: dict          # State updates to apply
```

**Responsibilities:**
- Analyze user requests and determine workflow stage
- Route work to the appropriate agent
- Maintain ProjectState consistency
- Track progress through workflow
- Make stage transitions (planning → research → implementation → review → deployment)

**Decision Logic:**
- If no planned tasks → route to Planner
- If no research findings → route to Researcher
- If no code changes → route to Coder
- If no test results → route to Reviewer
- If review complete → route to Deployer

**System Prompt Highlights:**
```
You are the Orchestrator Agent - the lead coordinator.
Break down user requests into a workflow.
Assign tasks to the right agents.
Maintain shared ProjectState.
```

**Context Providers:** Full ProjectState

---

### 2. Planner Agent

**Role:** Task breakdown specialist - decomposes requirements, designs schemas

**Input Schema: `PlannerInput`**
```python
class PlannerInput(BaseIOSchema):
    user_request: str          # User requirement
    project_context: ProjectState  # Current state
```

**Output Schema: `PlannerOutput`**
```python
class PlannerOutput(BaseIOSchema):
    tasks: List[PlannedTask]                    # 2-5 concrete tasks
    schemas: List[SchemaDef]                    # Required schemas
    estimated_timeline: str                     # Effort estimate
    risks: List[str]                            # Identified risks
    recommendations: List[str]                  # Planning recommendations
```

**PlannedTask Structure:**
```python
class PlannedTask(BaseModel):
    task_id: str                                # Unique ID
    title: str                                  # Task title
    description: str                            # Detailed description
    acceptance_criteria: List[AcceptanceCriteria]  # Verifiable criteria
    estimated_effort: str                       # small/medium/large
    schema_definitions: Dict[str, Any]          # Required schemas
    dependencies: List[str]                     # Task IDs depended on
    assigned_to: Optional[str]                  # Agent assignment
    status: TaskStatus                          # Current status
```

**AcceptanceCriteria Structure:**
```python
class AcceptanceCriteria(BaseModel):
    criterion: str                              # The criterion
    verified: bool = False                      # Is it verified?
    verified_by: Optional[str]                  # Which agent verified?
```

**Responsibilities:**
- Break down requirement into 2-5 concrete, testable tasks
- Define 3-5 acceptance criteria per task
- Design input/output schemas for implementation
- Identify task dependencies
- Assess risks and effort

**System Prompt Highlights:**
```
You are the Planner Agent - strategic task breakdown specialist.
Decompose requirements into concrete tasks.
Design schemas for other agents.
Define clear acceptance criteria.
```

**Context Providers:** ProjectState

**Example Output:**
```python
tasks = [
    PlannedTask(
        task_id="task-1",
        title="Create User Schema",
        description="Design Pydantic schema for user data",
        acceptance_criteria=[
            AcceptanceCriteria(criterion="Schema has required fields"),
            AcceptanceCriteria(criterion="Field types are correct"),
            AcceptanceCriteria(criterion="Validation rules present"),
        ],
        estimated_effort="small"
    ),
]
```

---

### 3. Researcher Agent

**Role:** Context specialist - gathers documentation, analyzes constraints

**Input Schema: `ResearcherInput`**
```python
class ResearcherInput(BaseIOSchema):
    research_topic: str                 # What to research
    project_context: ProjectState       # Current state
    sources_to_check: List[str] = []   # Files to review
```

**Output Schema: `ResearcherOutput`**
```python
class ResearcherOutput(BaseIOSchema):
    findings: ResearchFindings          # Key findings
    documentation_review: dict          # Docs reviewed
    architecture_notes: str             # Codebase architecture
    integration_points: List[str]       # How to integrate
    next_steps: List[str]              # Recommendations
```

**ResearchFindings Structure:**
```python
class ResearchFindings(BaseModel):
    topic: str                          # Research topic
    findings: List[str]                 # Key findings
    sources: List[str]                  # Source documents
    constraints: List[str]              # Constraints discovered
    recommendations: List[str]          # Recommendations
    context: Dict[str, Any]             # Additional context
```

**Responsibilities:**
- Review project documentation
- Analyze framework patterns (from atomic-agents examples)
- Document constraints: APIs, compatibility, architecture rules
- Map integration points with existing code
- Identify potential blockers

**System Prompt Highlights:**
```
You are the Researcher Agent - context and documentation specialist.
Gather information before implementation.
Analyze requirements and codebase.
Bridge user needs with framework capabilities.
```

**Context Providers:** ProjectState, TaskContext

**Example Output:**
```python
findings = ResearchFindings(
    topic="User authentication implementation",
    findings=[
        "atomic-agents supports custom context providers",
        "Pydantic BaseModel validation is built-in",
        "SystemPromptGenerator handles dynamic prompts"
    ],
    constraints=[
        "Max 100k context tokens",
        "Must follow atomic modularity principles"
    ],
    recommendations=[
        "Use context providers for state injection",
        "Follow BaseTool pattern for operations"
    ]
)
```

---

### 4. Coder Agent

**Role:** Implementation specialist - writes TDD code

**Input Schema: `CoderInput`**
```python
class CoderInput(BaseIOSchema):
    implementation_task: str            # What to implement
    project_context: ProjectState       # Current state
    schemas: dict = {}                  # Schema definitions
    constraints: List[str] = []         # Implementation constraints
```

**Output Schema: `CoderOutput`**
```python
class CoderOutput(BaseIOSchema):
    code_changes: List[CodeChange]      # Files changed
    test_cases: List[TestCase]          # Test cases (TDD)
    implementation_notes: str           # Implementation notes
    decisions_made: List[str]           # Key decisions
    potential_issues: List[str]         # Known issues
    code_structure: str                 # Code organization summary
```

**CodeChange Structure:**
```python
class CodeChange(BaseModel):
    file_path: str                      # File path
    change_type: str                    # create/modify/delete
    original_content: Optional[str]     # Original content
    new_content: Optional[str]          # New content
    description: str                    # What changed
    tdd_test_first: bool = True        # Tests written first?
    tests_added: List[str]             # Test function names
```

**TestCase Structure:**
```python
class TestCase(BaseModel):
    test_name: str                      # Test name
    test_code: str                      # Test code (pytest)
    purpose: str                        # What it validates
```

**Responsibilities:**
- Write tests FIRST (TDD approach)
- Implement code to make tests pass
- Follow atomic-agents patterns (BaseIOSchema, BaseTool, AtomicAgent)
- Use type hints and Pydantic schemas
- Document decisions and edge cases

**TDD Pattern:**
1. Read acceptance criteria from Planner output
2. Write test for each criterion (test_code)
3. Implement code to pass tests
4. Each test validates one acceptance criterion

**System Prompt Highlights:**
```
You are the Coder Agent - implementation specialist.
Follow Test-Driven Development (TDD): tests first!
Write production-ready, type-safe code.
Follow atomic-agents patterns and best practices.
```

**Context Providers:** ProjectState, TaskContext, ResearchContext

**Example Output:**
```python
code_changes = [
    CodeChange(
        file_path="src/user_schema.py",
        change_type="create",
        new_content="""
from atomic_agents import BaseIOSchema
from pydantic import Field

class UserSchema(BaseIOSchema):
    # Detailed implementation
    ...
""",
        tdd_test_first=True,
        tests_added=["test_user_schema_required_fields"]
    )
]

test_cases = [
    TestCase(
        test_name="test_user_schema_required_fields",
        test_code="""
def test_user_schema_required_fields():
    with pytest.raises(ValidationError):
        UserSchema()  # Should fail - required fields missing
""",
        purpose="Validates that required fields are enforced"
    )
]
```

---

### 5. Reviewer Agent

**Role:** Quality and security gatekeeper - tests, audits, validates

**Input Schema: `ReviewerInput`**
```python
class ReviewerInput(BaseIOSchema):
    code_to_review: str                 # Code to review
    project_context: ProjectState       # Current state
    test_cases: List[str] = []         # Test cases to run
```

**Output Schema: `ReviewerOutput`**
```python
class ReviewerOutput(BaseIOSchema):
    test_results: List[TestResult]      # Test execution results
    overall_test_pass: bool             # All tests pass?
    test_coverage: float                # Code coverage %
    
    security_findings: List[SecurityAuditFinding]  # Vulnerabilities
    quality_issues: List[QualityIssue]  # Quality problems
    quality_score: float                # 0-100 quality score
    
    acceptance_criteria_met: bool       # All criteria pass?
    review_passed: bool                 # Approve deployment?
    blockers: List[str]                 # Must-fix issues
    recommendations: List[str]          # Nice-to-have improvements
```

**TestResult Structure:**
```python
class TestResult(BaseModel):
    test_name: str                      # Test name
    status: str                         # passed/failed/skipped
    duration_ms: float                  # Execution time
    output: str                         # Test output
    coverage_percent: Optional[float]   # Coverage %
```

**SecurityAuditFinding Structure:**
```python
class SecurityAuditFinding(BaseModel):
    severity: str                       # critical/high/medium/low
    category: str                       # OWASP category
    file_path: str                      # Affected file
    line_number: Optional[int]          # Line number
    description: str                    # Vulnerability description
    remediation: str                    # How to fix
    status: str = "open"               # open/remediated/accepted_risk
```

**QualityIssue Structure:**
```python
class QualityIssue(BaseModel):
    severity: str                       # low/medium/high/critical
    category: str                       # style/complexity/maintainability
    file_path: str                      # Affected file
    line_number: Optional[int]          # Line number
    description: str                    # What's wrong?
    suggestion: str                     # How to fix?
```

**Review Pass Criteria:**
- All tests pass (100% for critical, ≥80% overall)
- Test coverage ≥80%
- No critical or high security issues
- All acceptance criteria verified
- Quality score ≥75/100

**Responsibilities:**
- Execute test suite
- Measure code coverage
- Perform security audit
- Check code quality and style
- Verify acceptance criteria
- Make approval/rejection decision

**System Prompt Highlights:**
```
You are the Reviewer Agent - quality and security gatekeeper.
Run tests and verify coverage.
Perform security audit for vulnerabilities.
Validate against acceptance criteria.
Decide: can this ship or needs fixes?
```

**Context Providers:** ProjectState, CodeContext, ReviewContext

**Example Output:**
```python
test_results = [
    TestResult(
        test_name="test_user_schema_required_fields",
        status="passed",
        duration_ms=125.5,
        coverage_percent=92.0
    )
]

security_findings = [
    SecurityAuditFinding(
        severity="high",
        category="SQL Injection",
        file_path="src/db.py",
        line_number=42,
        description="SQL query not parameterized",
        remediation="Use prepared statements or ORM"
    )
]

review_output = ReviewerOutput(
    test_results=test_results,
    overall_test_pass=True,
    test_coverage=92.0,
    security_findings=security_findings,
    quality_score=85.0,
    acceptance_criteria_met=True,
    review_passed=False,  # Blocked by security finding
    blockers=["Fix SQL injection in db.py:42"],
    recommendations=["Add type hints to util functions"]
)
```

---

### 6. Deployer Agent

**Role:** DevOps and optimization specialist - CI/CD, performance, documentation

**Input Schema: `DeployerInput`**
```python
class DeployerInput(BaseIOSchema):
    deployment_target: str = "staging"  # staging/production
    project_context: ProjectState       # Current state
    code_review_result: dict = {}      # Code review approval
```

**Output Schema: `DeployerOutput`**
```python
class DeployerOutput(BaseIOSchema):
    deployment_steps: List[DeploymentStep]      # Steps executed
    deployment_successful: bool                 # Did it succeed?
    deployment_environment: str                 # Where deployed
    
    performance_metrics: List[PerformanceMetric]  # Perf metrics
    optimization_notes: str                       # Optimizations
    
    generated_documentation: List[DocumentationAsset]  # Docs
    deployment_checklist: Dict[str, bool]       # Checklist status
    
    rollback_plan: str                          # Rollback procedure
    deployment_summary: str                     # Summary
```

**DeploymentStep Structure:**
```python
class DeploymentStep(BaseModel):
    step_name: str                      # Step name
    command: str                        # Command to run
    status: TaskStatus                  # PENDING/COMPLETED/FAILED
    output: Optional[str]               # Step output
    error: Optional[str]                # Error if failed
    duration_seconds: float             # Execution time
```

**PerformanceMetric Structure:**
```python
class PerformanceMetric(BaseModel):
    metric_name: str                    # e.g., "request_latency_ms"
    value: float                        # Measured value
    unit: str                           # Unit of measurement
    threshold: Optional[float]          # Expected threshold
    passed: Optional[bool]              # Did metric pass?
```

**DocumentationAsset Structure:**
```python
class DocumentationAsset(BaseModel):
    file_name: str                      # Name of doc file
    content: str                        # Markdown content
    asset_type: str                     # api/guide/example/architecture
```

**Responsibilities:**
- Execute deployment steps (build, test, package, deploy)
- Verify pre-deployment checklist
- Measure performance metrics
- Optimize code if needed
- Generate user-facing documentation
- Create rollback plan

**Deployment Checklist:**
- ✓ Code review passed
- ✓ All tests pass
- ✓ Security audit passed
- ✓ Documentation generated
- ✓ Performance metrics acceptable
- ✓ Rollback plan ready

**System Prompt Highlights:**
```
You are the Deployer Agent - DevOps specialist.
Prepare code for production.
Run CI/CD steps.
Measure performance and optimize.
Generate documentation for users.
```

**Context Providers:** ProjectState, ReviewContext, CodeContext

**Example Output:**
```python
deployment_steps = [
    DeploymentStep(
        step_name="Build Docker image",
        command="docker build -t myapp:v1.0 .",
        status=TaskStatus.COMPLETED,
        output="Successfully built",
        duration_seconds=45.0
    ),
    DeploymentStep(
        step_name="Push to registry",
        command="docker push myapp:v1.0",
        status=TaskStatus.COMPLETED,
        output="Pushed",
        duration_seconds=30.0
    )
]

performance_metrics = [
    PerformanceMetric(
        metric_name="request_latency_ms",
        value=125.5,
        unit="ms",
        threshold=200.0,
        passed=True
    )
]

generated_documentation = [
    DocumentationAsset(
        file_name="CHANGELOG.md",
        content="# v1.0 Release\n\n## Features\n...",
        asset_type="guide"
    )
]

deployer_output = DeployerOutput(
    deployment_steps=deployment_steps,
    deployment_successful=True,
    deployment_environment="production",
    performance_metrics=performance_metrics,
    generated_documentation=generated_documentation,
    deployment_checklist={
        "Code review": True,
        "Tests": True,
        "Security": True,
        "Documentation": True,
        "Performance": True
    },
    rollback_plan="docker service update --image myapp:v0.9 myapp"
)
```

---

## Communication Protocols

### Agent Handoff Protocol

When one agent completes work and hands off to the next:

1. **Current Agent Completes Work**
   - Reads ProjectState via context providers
   - Processes task using tools
   - Generates typed output schema
   - Updates ProjectState with results

2. **Update Shared State**
   ```python
   # Agent updates state with results
   state.planned_tasks = planner_output.tasks
   state.research_findings = researcher_output.findings
   state.code_changes = coder_output.code_changes
   # ... etc
   ```

3. **Orchestrator Routes Next Agent**
   ```python
   orch_output = orchestrator.run(OrchestratorInput(
       user_request=request,
       current_state=state
   ))
   next_agent = orch_output.next_agent
   ```

4. **Next Agent Reads Context**
   ```python
   # Context providers inject state
   agent.register_context_provider("project_state", ProjectStateContextProvider(state))
   agent.register_context_provider("task_context", TaskContextProvider(state))
   # State automatically injected into system prompt
   ```

5. **Execute and Loop**
   ```python
   output = next_agent.run(input_obj)
   state = parse_output_to_state(output, state)
   # Back to step 3
   ```

### Context Provider Injection

Each agent receives relevant context automatically:

```python
# Planner sees full project state
ProjectStateContextProvider(state)

# Coder sees task details, research, and previous results
TaskContextProvider(state)
ResearchContextProvider(state)
CodeContextProvider(state)

# Reviewer sees code and quality context
CodeContextProvider(state)
ReviewContextProvider(state)

# Deployer sees review results
ReviewContextProvider(state)
CodeContextProvider(state)
ProjectStateContextProvider(state)
```

### Error Handling

If an agent fails:

```python
try:
    output = agent.run(input_obj)
    state = parse_output_to_state(output, state)
except Exception as e:
    state.errors.append(f"{agent_name}: {str(e)}")
    state.workflow_stage = "blocked"
    return state
```

---

## Execution Workflows

### Workflow 1: New Feature Development

```
User: "Add user authentication with JWT tokens"

Orchestrator → Determine stage: PLANNING
↓
Planner → Break down:
  - Task 1: Design JWT schema
  - Task 2: Create auth endpoints
  - Task 3: Add token validation
  - Task 4: Integrate with API

Orchestrator → Determine stage: RESEARCH
↓
Researcher → Analyze:
  - How JWT works
  - Framework support
  - Security best practices
  - Integration points

Orchestrator → Determine stage: IMPLEMENTATION
↓
Coder → Implement:
  - Write tests for each task (TDD)
  - Implement JWT schema
  - Implement auth endpoints
  - Integrate validation

Orchestrator → Determine stage: REVIEW
↓
Reviewer → Validate:
  - All tests pass?
  - Coverage ≥80%?
  - Security audit passed?
  - All acceptance criteria met?

Orchestrator → Determine stage: DEPLOYMENT
↓
Deployer → Deploy:
  - Build and test
  - Deploy to staging
  - Measure performance
  - Generate user docs
  - Create rollback plan

Final State: ProjectState with all results
```

### Workflow 2: Bug Fix

```
User: "Fix: User profile images not loading on mobile"

Planner → 
  - Task 1: Identify root cause
  - Task 2: Fix image loading logic
  - Task 3: Add mobile tests

Researcher →
  - Check mobile guidelines
  - Review image handling code
  - Find relevant examples

Coder →
  - TDD: Write mobile-specific tests
  - Fix responsive image loading
  - Add mobile viewport tests

Reviewer →
  - Test on multiple devices
  - Verify performance
  - Check CSS media queries

Deployer →
  - Deploy fix
  - Monitor image loading metrics
  - Document in release notes
```

### Workflow 3: Security Patch

```
User: "Apply security patch for dependency vulnerability"

Planner →
  - Task 1: Update dependency
  - Task 2: Verify compatibility
  - Task 3: Run security tests

Researcher →
  - Analyze vulnerability
  - Check compatibility matrix
  - Review migration guide

Coder →
  - Update lock files
  - Test for breaking changes
  - Add regression tests

Reviewer →
  - Run full test suite
  - Security audit updated code
  - Verify no vulnerabilities remain

Deployer →
  - Deploy to staging first
  - Monitor for issues
  - Deploy to production
  - Update security docs
```

---

## Installation & Setup

### Prerequisites

- Python 3.12+
- pip or uv package manager
- LLM API key (OpenAI, Anthropic, or Groq)

### Step 1: Install atomic-agents

```bash
# Using pip
pip install atomic-agents>=2.2.0
pip install instructor>=1.3.0

# Using uv (recommended)
uv add atomic-agents
uv add instructor
```

### Step 2: Install provider SDK

Choose your LLM provider:

```bash
# OpenAI (default)
pip install openai>=1.40.0
export OPENAI_API_KEY="sk-..."

# OR Anthropic
pip install anthropic>=0.25.0
export ANTHROPIC_API_KEY="sk-ant-..."

# OR Groq
pip install groq>=0.4.0
export GROQ_API_KEY="gsk_..."
```

### Step 3: Install agent team dependencies

```bash
cd /home/user/atomic-agents
pip install -e .
pip install python-dotenv
```

### Step 4: Set up environment

Create `.env` file in project root:

```env
# For OpenAI
OPENAI_API_KEY=sk-...

# For Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# For Groq
GROQ_API_KEY=gsk_...

# Optional: Model overrides
DEFAULT_PROVIDER=openai
DEFAULT_MODEL=gpt-4o-mini
```

### Step 5: Verify installation

```bash
# Test imports
python -c "from atomic_agents.agents.atomic_agents import AtomicAgent; print('✓ atomic-agents installed')"

# Test agent team
cd .claude/agents
python main.py --request "Test request" --verbose
```

### Step 6: Initialize agent team (Optional)

```bash
# Initialize team configuration
python -m claude.agents.main --init

# View team configuration
cat config.json
```

---

## Usage Examples

### Example 1: Run a complete workflow from CLI

```bash
cd /home/user/atomic-agents

python -m claude.agents.main \
    --request "Add email verification to user signup" \
    --project "my-auth-app" \
    --provider openai \
    --verbose
```

Output:
```
🚀 Starting workflow: Add email verification to user signup
   Project: my-auth-app

📍 Stage 1: planning
   Planning tasks and schemas...
   ✓ Planned 4 tasks

📍 Stage 2: research
   Researching requirements and constraints...
   ✓ Research findings: 8 key points

📍 Stage 3: implementation
   Writing code and tests...
   ✓ Code changes: 5 files
   ✓ Test cases: 12 tests (TDD)

📍 Stage 4: review
   Reviewing code, running tests, security audit...
   ✓ Tests: 12 (pass: True)
   ✓ Coverage: 92%
   ✓ Quality Score: 88/100

📍 Stage 5: deployment
   Deploying and optimizing...
   ✓ Deployment: True
   ✓ Documentation: 3 assets

🎉 Workflow complete!
============================================================
PROJECT: my-auth-app
============================================================
Tasks Planned:    4
Code Files:       5
Tests Written:    12
Test Coverage:    92%
Code Quality:     88/100
Security Issues:  0
Deployment:       completed
============================================================

💾 State saved to: my-auth-app_state.json
```

### Example 2: Use programmatically in Python

```python
from claude.agents.main import AgentTeam

# Create team with OpenAI
team = AgentTeam(provider="openai", model="gpt-4o", verbose=True)

# Run workflow
state = team.run_workflow(
    user_request="Create a caching layer for database queries",
    project_name="cache-service",
    project_description="Performance optimization project"
)

# Access results
print(f"Tasks planned: {len(state.planned_tasks)}")
print(f"Code files: {len(state.code_changes)}")
print(f"Test coverage: {state.test_coverage}%")
print(f"Quality score: {state.code_quality_score}/100")
print(f"Deployment status: {state.deployment_status}")

# Save final state
import json
with open("cache-service_final_state.json", "w") as f:
    json.dump(state.dict(), f, indent=2, default=str)
```

### Example 3: Use specific agents individually

```python
from claude.agents.planner import create_planner_agent, PlannerInput
from claude.agents.shared_state import ProjectState
import instructor
from openai import OpenAI

# Create client and agent
client = instructor.from_openai(OpenAI())
planner = create_planner_agent(client, model="gpt-4o-mini")

# Create initial state
state = ProjectState(
    project_name="feature-x",
    project_description="Add export to PDF",
    user_request="Add PDF export functionality"
)

# Run just the planner
planner_input = PlannerInput(
    user_request=state.user_request,
    project_context=state
)

planner_output = planner.run(planner_input)

# Process output
for task in planner_output.tasks:
    print(f"Task: {task.title}")
    for criterion in task.acceptance_criteria:
        print(f"  - {criterion.criterion}")
```

### Example 4: Use with Anthropic

```bash
python -m claude.agents.main \
    --request "Implement role-based access control" \
    --project "rbac-system" \
    --provider anthropic \
    --model claude-3-5-sonnet-20241022 \
    --verbose
```

### Example 5: Use with Groq for speed

```bash
python -m claude.agents.main \
    --request "Add dark mode toggle" \
    --project "ui-enhancement" \
    --provider groq \
    --model mixtral-8x7b-32768 \
    --verbose
```

---

## API Reference

### Core Classes

#### ProjectState

```python
from claude.agents.shared_state import ProjectState

state = ProjectState(
    project_name="my-project",
    project_description="Description here",
    user_request="Feature request"
)
```

#### Agent Team

```python
from claude.agents.main import AgentTeam

team = AgentTeam(
    provider="openai",           # openai, anthropic, groq
    model="gpt-4o-mini",         # Optional: override default
    verbose=True                 # Enable logging
)

state = team.run_workflow(
    user_request="Your request",
    project_name="project-name",
    project_description="Description"
)
```

#### Individual Agents

```python
from claude.agents.orchestrator import create_orchestrator_agent
from claude.agents.planner import create_planner_agent
from claude.agents.researcher import create_researcher_agent
from claude.agents.coder import create_coder_agent
from claude.agents.reviewer import create_reviewer_agent
from claude.agents.deployer import create_deployer_agent

agent = create_planner_agent(client, model="gpt-4o-mini")
output = agent.run(input_obj)
```

#### Tools

```python
from claude.agents.tools import (
    FileReadTool, FileWriteTool, DirectoryListTool,
    ShellExecuteTool, CodeAnalysisTool
)

tools = {
    "read_file": FileReadTool(),
    "write_file": FileWriteTool(),
    "list_directory": DirectoryListTool(),
    "execute_shell": ShellExecuteTool(),
    "analyze_code": CodeAnalysisTool(),
}
```

#### Context Providers

```python
from claude.agents.context_providers import (
    ProjectStateContextProvider,
    TaskContextProvider,
    ResearchContextProvider,
    CodeContextProvider,
    ReviewContextProvider
)

# Register on agents
agent.register_context_provider(
    "project_state",
    ProjectStateContextProvider(state)
)
```

---

## Best Practices

### For Using the Agent Team

1. **Clear Requests**
   - Provide specific, detailed requirements
   - Include acceptance criteria if possible
   - Mention constraints upfront

2. **Monitor Progress**
   - Use `--verbose` flag to see each stage
   - Check generated state files for detailed results
   - Review errors and warnings

3. **Iterative Refinement**
   - If review fails, analyzer provides specific blockers
   - Re-run with refined request after fixes
   - Use planner output to understand scope

4. **Provider Selection**
   - Use Opus/Claude for complex reasoning (orchestrator)
   - Use faster models for focused tasks (coder, reviewer)
   - Consider cost vs. quality tradeoffs

### For Extending the System

1. **Adding New Agents**
   - Create new agent module in `.claude/agents/`
   - Define Input/Output schemas (inherit from BaseIOSchema)
   - Implement create_*_agent() factory function
   - Add to AgentTeam.agents dict
   - Update orchestrator routing logic

2. **Adding New Tools**
   - Inherit from BaseTool[InputSchema, OutputSchema]
   - Implement run(params: InputSchema) -> OutputSchema
   - Add safety checks for shell commands
   - Register with agents in main.py

3. **Custom Context Providers**
   - Inherit from BaseDynamicContextProvider
   - Implement get_info() -> str
   - Register on agents that need the context
   - Context auto-injected into system prompt

4. **Modifying Workflows**
   - Edit `determine_next_stage()` in orchestrator.py
   - Update workflow stages in config.json
   - Adjust agent queue order
   - Test with `--verbose` flag

### Security Considerations

1. **API Keys**
   - Store in `.env` file (never commit!)
   - Use environment variables
   - Consider using secret management service

2. **Tool Safety**
   - ShellExecuteTool has whitelist of allowed commands
   - Adds timeouts to prevent hangs
   - Limits output to prevent token overflow
   - Add `--dry-run` mode for preview

3. **Code Review**
   - All code runs through reviewer before deployment
   - Security audit checks for common vulnerabilities
   - Coverage thresholds prevent gaps
   - Manual review recommended for sensitive code

4. **State Management**
   - ProjectState saved to disk (JSON)
   - Contains no secrets (API keys, passwords)
   - Can be replayed for debugging
   - Versioned for auditing

---

## Troubleshooting

### Agent Fails to Initialize

```
Error: failed to create client
```

**Solution:** Check LLM API key is set correctly
```bash
echo $OPENAI_API_KEY  # Should show your key
```

### Review Fails with High Security Issues

```
review_passed: False
blockers: ["SQL injection in db.py:42"]
```

**Solution:** Fix identified issues and re-run coder for that task
```python
# Coder will fix and provide updated code
```

### Out of Context Tokens

```
Error: Token limit exceeded
```

**Solution:** Increase `max_context_tokens` in config or split into smaller tasks

### Workflow Hangs

```
Stage not progressing...
```

**Solution:** Check for infinite loops or stuck processes
```bash
# Use timeout
timeout 300 python -m claude.agents.main --request "..."

# Check logs for errors
grep -i error *.log
```

---

## Resources

- **Atomic Agents Framework:** https://github.com/BrainBlend-AI/atomic-agents
- **Framework Documentation:** https://brainblend-ai.github.io/atomic-agents/
- **Instructor Library:** https://python.useinstructor.com/
- **Pydantic:** https://docs.pydantic.dev/latest/

---

## License

This agent team system is part of atomic-agents and is MIT licensed.

---

## Contributing

To contribute improvements to the agent team:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

Feedback and improvements welcome!

---

**Last Updated:** 2026-05-18  
**Version:** 1.0.0  
**Status:** Production Ready
