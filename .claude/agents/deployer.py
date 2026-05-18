"""Deployer/Optimizer Agent - CI/CD, performance optimization, and documentation."""

from pydantic import Field
from typing import List, Optional, Dict, Any
from atomic_agents import (
    BaseIOSchema, AtomicAgent, AgentConfig, BaseTool
)
from atomic_agents.context import SystemPromptGenerator
from .shared_state import ProjectState, DeploymentStep, TaskStatus
from .context_providers import (
    ProjectStateContextProvider,
    ReviewContextProvider,
    CodeContextProvider
)


# ============================================================================
# DEPLOYER SCHEMAS
# ============================================================================

class DeployerInput(BaseIOSchema):
    """Input to deployer agent."""
    deployment_target: str = Field(
        default="staging",
        description="Where to deploy: staging, production, etc."
    )
    project_context: ProjectState = Field(..., description="Current project state")
    code_review_result: dict = Field(
        default_factory=dict,
        description="Code review results and approval"
    )


class DocumentationAsset(BaseIOSchema):
    """Documentation asset to generate."""
    file_name: str = Field(..., description="Name of documentation file")
    content: str = Field(..., description="Markdown or text content")
    asset_type: str = Field(..., description="api, guide, example, architecture")


class PerformanceMetric(BaseIOSchema):
    """Performance metric measured."""
    metric_name: str = Field(..., description="Name of metric")
    value: float = Field(..., description="Measured value")
    unit: str = Field(..., description="Unit of measurement")
    threshold: Optional[float] = Field(None, description="Expected threshold")
    passed: Optional[bool] = Field(None, description="Did metric meet threshold?")


class DeployerOutput(BaseIOSchema):
    """Output from deployer agent."""
    deployment_steps: List[DeploymentStep] = Field(
        ...,
        description="Deployment steps executed"
    )
    deployment_successful: bool = Field(..., description="Did deployment succeed?")
    deployment_environment: str = Field(..., description="Where deployed")

    performance_metrics: List[PerformanceMetric] = Field(
        default_factory=list,
        description="Performance metrics measured"
    )
    optimization_notes: str = Field(
        default="",
        description="Notes on optimizations made"
    )

    generated_documentation: List[DocumentationAsset] = Field(
        default_factory=list,
        description="Generated documentation"
    )

    deployment_checklist: Dict[str, bool] = Field(
        default_factory=dict,
        description="Deployment checklist items and status"
    )

    rollback_plan: str = Field(
        default="",
        description="If needed, how to rollback"
    )

    deployment_summary: str = Field(
        default="",
        description="Summary of deployment and changes"
    )


# ============================================================================
# DEPLOYER AGENT FACTORY
# ============================================================================

def create_deployer_agent(
    client,
    model: str = "gpt-4o-mini",
    tools: Optional[List[BaseTool]] = None
) -> AtomicAgent[DeployerInput, DeployerOutput]:
    """Create the deployer/optimizer agent."""

    system_prompt = SystemPromptGenerator(
        background=[
            "You are the Deployer Agent - the DevOps and optimization specialist.",
            "Your role is to prepare code for production deployment.",
            "You handle CI/CD orchestration, performance optimization, and documentation generation.",
            "You ensure code is production-ready and users understand what changed.",
            "You think about scalability, monitoring, and rollback strategies.",
        ],
        steps=[
            "1. Verify code has passed review and all checks passed",
            "2. Execute deployment steps (build, test, package, deploy)",
            "3. Measure performance metrics against baselines",
            "4. Identify and implement optimizations where needed",
            "5. Generate comprehensive documentation for the changes",
            "6. Create deployment checklist and rollback plan",
            "7. Provide deployment summary and next steps",
        ],
        output_instructions=[
            "List deployment steps in order with clear descriptions",
            "Include performance metrics even if they all pass",
            "Generate documentation that helps users understand what's new",
            "Deployment checklist should cover: code review ✓, tests ✓, security ✓, docs ✓",
            "Always provide a rollback plan in case of issues",
            "Note any performance improvements or optimizations made",
            "Include links to relevant documentation and monitoring dashboards",
        ],
    )

    agent = AtomicAgent[DeployerInput, DeployerOutput](
        config=AgentConfig(
            client=client,
            model=model,
            system_prompt_generator=system_prompt,
        )
    )

    return agent


# ============================================================================
# DEPLOYER HELPERS
# ============================================================================

def parse_deployer_output_to_state(
    deployer_output: DeployerOutput,
    state: ProjectState
) -> ProjectState:
    """Convert deployer output into state updates."""
    state.deployment_steps = deployer_output.deployment_steps
    state.deployment_status = (
        TaskStatus.COMPLETED if deployer_output.deployment_successful
        else TaskStatus.FAILED
    )
    state.performance_metrics = {
        m.metric_name: m.value for m in deployer_output.performance_metrics
    }
    state.generated_documentation = {
        doc.file_name: doc.content for doc in deployer_output.generated_documentation
    }
    state.deployed_at = __import__('datetime').datetime.utcnow()
    state.workflow_stage = "deployment"
    return state


def generate_deployment_summary(state: ProjectState) -> str:
    """Generate human-readable deployment summary."""
    lines = [
        f"# Deployment Summary: {state.project_name}",
        "",
        f"**Status:** {state.deployment_status.value}",
        f"**Date:** {state.deployed_at}",
        "",
        f"## Changes ({len(state.code_changes)} files modified)",
    ]

    for change in state.code_changes:
        lines.append(f"- {change.file_path}: {change.description}")

    if state.test_results:
        lines.extend([
            "",
            f"## Tests ({len(state.test_results)} total)",
            f"- Passed: {sum(1 for t in state.test_results if t.status == 'passed')}",
            f"- Failed: {sum(1 for t in state.test_results if t.status == 'failed')}",
            f"- Coverage: {state.test_coverage}%",
        ])

    if state.performance_metrics:
        lines.extend([
            "",
            "## Performance Metrics",
        ])
        for name, value in state.performance_metrics.items():
            lines.append(f"- {name}: {value}")

    return "\n".join(lines)
