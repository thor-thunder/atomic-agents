"""Shared state model for 6-agent atomic team coordination."""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Status of task execution."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class AcceptanceCriteria(BaseModel):
    """Acceptance criteria for a task."""
    criterion: str = Field(..., description="The acceptance criterion")
    verified: bool = Field(default=False, description="Whether criterion is met")
    verified_by: Optional[str] = Field(default=None, description="Which agent verified this")


class PlannedTask(BaseModel):
    """A task planned by the planner agent."""
    task_id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Detailed description")
    acceptance_criteria: List[AcceptanceCriteria] = Field(default_factory=list)
    estimated_effort: str = Field(..., description="Estimated effort (e.g., 'small', 'medium', 'large')")
    schema_definitions: Dict[str, Any] = Field(
        default_factory=dict,
        description="Input/output schemas needed"
    )
    dependencies: List[str] = Field(default_factory=list, description="Task IDs this depends on")
    assigned_to: Optional[str] = Field(default=None, description="Agent assigned to task")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)


class ResearchFindings(BaseModel):
    """Findings from researcher agent."""
    topic: str = Field(..., description="What was researched")
    findings: List[str] = Field(default_factory=list, description="Key findings")
    sources: List[str] = Field(default_factory=list, description="Source documents/files")
    constraints: List[str] = Field(default_factory=list, description="Constraints discovered")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class CodeChange(BaseModel):
    """A code change made by coder agent."""
    file_path: str = Field(..., description="File being changed")
    change_type: str = Field(..., description="Type: 'create', 'modify', 'delete'")
    original_content: Optional[str] = Field(default=None, description="Original file content")
    new_content: Optional[str] = Field(default=None, description="New file content")
    description: str = Field(..., description="Description of change")
    tdd_test_first: bool = Field(default=True, description="Was test written first?")
    tests_added: List[str] = Field(default_factory=list, description="Test functions added")


class TestResult(BaseModel):
    """Test result from reviewer agent."""
    test_name: str = Field(..., description="Test name")
    status: str = Field(..., description="passed, failed, skipped")
    duration_ms: float = Field(..., description="Test duration in milliseconds")
    output: str = Field(default="", description="Test output/error")
    coverage_percent: Optional[float] = Field(default=None, description="Code coverage %")


class SecurityAuditFinding(BaseModel):
    """Security finding from reviewer agent."""
    severity: str = Field(..., description="critical, high, medium, low")
    category: str = Field(..., description="OWASP category or vulnerability type")
    file_path: str = Field(..., description="Affected file")
    line_number: Optional[int] = Field(default=None)
    description: str = Field(..., description="Vulnerability description")
    remediation: str = Field(..., description="How to fix")
    status: str = Field(default="open", description="open, remediated, accepted_risk")


class DeploymentStep(BaseModel):
    """A deployment step from deployer agent."""
    step_name: str = Field(..., description="Name of deployment step")
    command: str = Field(..., description="Command to run")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    output: Optional[str] = Field(default=None)
    error: Optional[str] = Field(default=None)
    duration_seconds: float = Field(default=0.0)


class ProjectState(BaseModel):
    """Shared state maintained by all 6 agents."""

    # Project identification
    project_name: str = Field(..., description="Name of project")
    project_description: str = Field(default="", description="Project description")

    # Initial requirement
    user_request: str = Field(default="", description="Original user request")

    # Planner outputs
    planned_tasks: List[PlannedTask] = Field(
        default_factory=list,
        description="Tasks planned by planner agent"
    )

    # Researcher outputs
    research_findings: List[ResearchFindings] = Field(
        default_factory=list,
        description="Findings from researcher agent"
    )
    research_completed_at: Optional[datetime] = Field(default=None)

    # Coder outputs
    code_changes: List[CodeChange] = Field(
        default_factory=list,
        description="Code changes by coder agent"
    )
    implementation_status: TaskStatus = Field(default=TaskStatus.PENDING)

    # Reviewer outputs
    test_results: List[TestResult] = Field(
        default_factory=list,
        description="Test results from reviewer"
    )
    test_coverage: float = Field(default=0.0, description="Overall test coverage %")
    security_audit_findings: List[SecurityAuditFinding] = Field(
        default_factory=list,
        description="Security issues found"
    )
    code_quality_score: float = Field(default=0.0, description="Code quality score 0-100")
    review_status: TaskStatus = Field(default=TaskStatus.PENDING)
    reviewed_by: str = Field(default="reviewer-agent")
    reviewed_at: Optional[datetime] = Field(default=None)

    # Deployer outputs
    deployment_steps: List[DeploymentStep] = Field(
        default_factory=list,
        description="Deployment steps executed"
    )
    deployment_status: TaskStatus = Field(default=TaskStatus.PENDING)
    performance_metrics: Dict[str, float] = Field(
        default_factory=dict,
        description="Performance metrics from deployment"
    )
    generated_documentation: Dict[str, str] = Field(
        default_factory=dict,
        description="Generated documentation (file_path -> content)"
    )
    deployed_at: Optional[datetime] = Field(default=None)

    # Orchestrator coordination
    current_agent: str = Field(default="orchestrator", description="Currently active agent")
    workflow_stage: str = Field(default="planning", description="Current workflow stage")
    errors: List[str] = Field(default_factory=list, description="Errors encountered")
    warnings: List[str] = Field(default_factory=list, description="Warnings")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
