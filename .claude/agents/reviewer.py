"""Reviewer/Validator Agent - Tests code, security audit, quality checks."""

from pydantic import Field
from typing import List, Optional
from atomic_agents import (
    BaseIOSchema, AtomicAgent, AgentConfig, BaseTool
)
from atomic_agents.context import SystemPromptGenerator
from .shared_state import (
    ProjectState,
    TestResult,
    SecurityAuditFinding,
    TaskStatus
)
from .context_providers import (
    ProjectStateContextProvider,
    CodeContextProvider,
    ReviewContextProvider
)


# ============================================================================
# REVIEWER SCHEMAS
# ============================================================================

class ReviewerInput(BaseIOSchema):
    """Input to reviewer agent."""
    code_to_review: str = Field(..., description="Code to review (file content or summary)")
    project_context: ProjectState = Field(..., description="Current project state")
    test_cases: List[str] = Field(
        default_factory=list,
        description="Test cases to execute"
    )


class TestExecutionResult(BaseIOSchema):
    """Result of test execution."""
    test_name: str = Field(..., description="Name of test")
    passed: bool = Field(..., description="Did test pass?")
    duration_ms: float = Field(..., description="Execution time")
    output: str = Field(default="", description="Test output/error")
    coverage_percent: float = Field(default=0.0, description="Coverage for this test")


class QualityIssue(BaseIOSchema):
    """Code quality issue found."""
    severity: str = Field(..., description="low, medium, high, critical")
    category: str = Field(..., description="e.g., 'style', 'complexity', 'maintainability'")
    file_path: str = Field(..., description="File with the issue")
    line_number: Optional[int] = Field(None, description="Line number if applicable")
    description: str = Field(..., description="What's wrong?")
    suggestion: str = Field(..., description="How to fix?")


class ReviewerOutput(BaseIOSchema):
    """Output from reviewer agent."""
    test_results: List[TestResult] = Field(..., description="Results from running tests")
    overall_test_pass: bool = Field(..., description="Do all tests pass?")
    test_coverage: float = Field(..., description="Overall code coverage %")

    security_findings: List[SecurityAuditFinding] = Field(
        default_factory=list,
        description="Security vulnerabilities found"
    )

    quality_issues: List[QualityIssue] = Field(
        default_factory=list,
        description="Code quality issues"
    )
    quality_score: float = Field(..., description="Overall quality score 0-100")

    acceptance_criteria_met: bool = Field(
        ...,
        description="Do all acceptance criteria from planning pass?"
    )

    review_passed: bool = Field(
        ...,
        description="Can this code be approved for deployment?"
    )

    blockers: List[str] = Field(
        default_factory=list,
        description="Blocking issues that must be fixed"
    )

    recommendations: List[str] = Field(
        default_factory=list,
        description="Suggestions for improvement (non-blocking)"
    )


# ============================================================================
# REVIEWER AGENT FACTORY
# ============================================================================

def create_reviewer_agent(
    client,
    model: str = "gpt-4o-mini",
    tools: Optional[List[BaseTool]] = None
) -> AtomicAgent[ReviewerInput, ReviewerOutput]:
    """Create the reviewer/validator agent."""

    system_prompt = SystemPromptGenerator(
        background=[
            "You are the Reviewer Agent - the quality and security gatekeeper.",
            "Your role is to ensure code is production-ready before deployment.",
            "You run tests, perform security audits, and validate against acceptance criteria.",
            "You think like a QA engineer and security expert combined.",
            "You decide whether code can proceed to deployment or needs fixes.",
        ],
        steps=[
            "1. Review the code changes and understand what was implemented",
            "2. Execute test cases - verify all tests pass and coverage is adequate",
            "3. Perform security audit - check for vulnerabilities, injection risks, etc.",
            "4. Check code quality - complexity, maintainability, style compliance",
            "5. Verify against acceptance criteria - is the spec fully met?",
            "6. Identify blockers (must fix) vs recommendations (nice to have)",
            "7. Make final decision: can this ship?",
        ],
        output_instructions=[
            "Test coverage should be >=80% for approval",
            "No critical or high-severity security issues for approval",
            "All acceptance criteria from planning must be verified",
            "Clearly separate blockers from recommendations",
            "Quality score: 0-100 based on all factors",
            "Be thorough but fair - focus on real issues, not style nitpicks",
            "If review_passed=false, explain exactly what needs fixing",
        ],
    )

    agent = AtomicAgent[ReviewerInput, ReviewerOutput](
        config=AgentConfig(
            client=client,
            model=model,
            system_prompt_generator=system_prompt,
        )
    )

    return agent


# ============================================================================
# REVIEWER HELPERS
# ============================================================================

def parse_reviewer_output_to_state(
    reviewer_output: ReviewerOutput,
    state: ProjectState
) -> ProjectState:
    """Convert reviewer output into state updates."""
    state.test_results = reviewer_output.test_results
    state.test_coverage = reviewer_output.test_coverage
    state.security_audit_findings = reviewer_output.security_findings
    state.code_quality_score = reviewer_output.quality_score
    state.review_status = TaskStatus.COMPLETED if reviewer_output.review_passed else TaskStatus.BLOCKED
    state.reviewed_at = __import__('datetime').datetime.utcnow()
    state.workflow_stage = "review"
    return state
