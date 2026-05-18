"""Atomic Agents 6-Team System - Professional orchestration for software development."""

from .shared_state import (
    ProjectState,
    PlannedTask,
    ResearchFindings,
    CodeChange,
    TestResult,
    SecurityAuditFinding,
    DeploymentStep,
    AcceptanceCriteria,
    TaskStatus,
)

from .context_providers import (
    ProjectStateContextProvider,
    TaskContextProvider,
    ResearchContextProvider,
    CodeContextProvider,
    ReviewContextProvider,
)

from .tools import (
    FileReadTool,
    FileWriteTool,
    DirectoryListTool,
    ShellExecuteTool,
    CodeAnalysisTool,
    create_agent_tools,
)

from .orchestrator import (
    create_orchestrator_agent,
    OrchestratorInput,
    OrchestratorOutput,
    determine_next_stage,
    get_agent_queue,
)

from .planner import (
    create_planner_agent,
    PlannerInput,
    PlannerOutput,
    SchemaDef,
)

from .researcher import (
    create_researcher_agent,
    ResearcherInput,
    ResearcherOutput,
)

from .coder import (
    create_coder_agent,
    CoderInput,
    CoderOutput,
    TestCase,
)

from .reviewer import (
    create_reviewer_agent,
    ReviewerInput,
    ReviewerOutput,
    TestExecutionResult,
    QualityIssue,
)

from .deployer import (
    create_deployer_agent,
    DeployerInput,
    DeployerOutput,
    DocumentationAsset,
    PerformanceMetric,
)

from .main import AgentTeam

__version__ = "1.0.0"
__author__ = "Atomic Agents Team"

__all__ = [
    # Core classes
    "AgentTeam",
    "ProjectState",
    "TaskStatus",

    # Schemas
    "PlannedTask",
    "AcceptanceCriteria",
    "ResearchFindings",
    "CodeChange",
    "TestResult",
    "SecurityAuditFinding",
    "DeploymentStep",

    # Orchestrator
    "create_orchestrator_agent",
    "OrchestratorInput",
    "OrchestratorOutput",
    "determine_next_stage",
    "get_agent_queue",

    # Planner
    "create_planner_agent",
    "PlannerInput",
    "PlannerOutput",
    "SchemaDef",

    # Researcher
    "create_researcher_agent",
    "ResearcherInput",
    "ResearcherOutput",

    # Coder
    "create_coder_agent",
    "CoderInput",
    "CoderOutput",
    "TestCase",

    # Reviewer
    "create_reviewer_agent",
    "ReviewerInput",
    "ReviewerOutput",
    "TestExecutionResult",
    "QualityIssue",

    # Deployer
    "create_deployer_agent",
    "DeployerInput",
    "DeployerOutput",
    "DocumentationAsset",
    "PerformanceMetric",

    # Context Providers
    "ProjectStateContextProvider",
    "TaskContextProvider",
    "ResearchContextProvider",
    "CodeContextProvider",
    "ReviewContextProvider",

    # Tools
    "FileReadTool",
    "FileWriteTool",
    "DirectoryListTool",
    "ShellExecuteTool",
    "CodeAnalysisTool",
    "create_agent_tools",
]
