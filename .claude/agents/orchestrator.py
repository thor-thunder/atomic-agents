"""Orchestrator/Lead Agent - Coordinates the 6-agent team."""

from pydantic import Field
from typing import List, Optional
from atomic_agents import (
    BaseIOSchema, AtomicAgent, AgentConfig, BaseTool
)
from atomic_agents.context import SystemPromptGenerator
from .shared_state import ProjectState, TaskStatus


# ============================================================================
# ORCHESTRATOR SCHEMAS
# ============================================================================

class AgentInstruction(BaseIOSchema):
    """Instruction for a specific agent."""
    target_agent: str = Field(
        ...,
        description="Which agent to instruct: planner, researcher, coder, reviewer, deployer"
    )
    task: str = Field(..., description="Task to perform")
    context: str = Field(default="", description="Additional context for the agent")
    priority: str = Field(default="normal", description="Priority: low, normal, high")


class OrchestratorInput(BaseIOSchema):
    """Input to orchestrator agent."""
    user_request: str = Field(..., description="User's request or task description")
    current_state: ProjectState = Field(..., description="Current project state")
    force_stage: Optional[str] = Field(
        None,
        description="Force workflow to specific stage (planning, research, implementation, review, deployment)"
    )


class OrchestratorOutput(BaseIOSchema):
    """Output from orchestrator agent."""
    next_agent: str = Field(
        ...,
        description="Which agent should execute next"
    )
    instruction: str = Field(..., description="Clear instruction for next agent")
    reasoning: str = Field(..., description="Why this agent/instruction was chosen")
    workflow_complete: bool = Field(False, description="Is workflow complete?")
    state_updates: dict = Field(default_factory=dict, description="State updates to apply")


# ============================================================================
# ORCHESTRATOR AGENT FACTORY
# ============================================================================

def create_orchestrator_agent(
    client,
    model: str = "gpt-4o-mini",
    tools: Optional[List[BaseTool]] = None
) -> AtomicAgent[OrchestratorInput, OrchestratorOutput]:
    """Create the orchestrator/lead agent."""

    system_prompt = SystemPromptGenerator(
        background=[
            "You are the Orchestrator Agent - the lead coordinator of a 6-agent team.",
            "Your role is to break down user requests into a workflow, assign tasks to the right agents, and track progress.",
            "You have 5 specialist agents available: Planner, Researcher, Coder, Reviewer, and Deployer.",
            "You maintain the shared ProjectState and ensure smooth handoffs between agents.",
        ],
        steps=[
            "1. Analyze the user request and current project state",
            "2. Determine the appropriate workflow stage (planning → research → implementation → review → deployment)",
            "3. Decide which agent should execute next based on state and workflow stage",
            "4. Provide clear, actionable instructions for the next agent",
            "5. Consider dependencies: research must precede coding, tests before deployment",
        ],
        output_instructions=[
            "Always specify exactly which agent should execute next",
            "Provide detailed context so the agent understands the goal",
            "If workflow is complete, set workflow_complete=true",
            "Suggest any state updates needed before the next agent runs",
        ],
    )

    agent = AtomicAgent[OrchestratorInput, OrchestratorOutput](
        config=AgentConfig(
            client=client,
            model=model,
            system_prompt_generator=system_prompt,
        )
    )

    return agent


# ============================================================================
# WORKFLOW HELPERS
# ============================================================================

def determine_next_stage(current_state: ProjectState, user_request: str) -> str:
    """Determine the next workflow stage based on current state."""
    if not current_state.planned_tasks:
        return "planning"
    elif not current_state.research_findings:
        return "research"
    elif not current_state.code_changes:
        return "implementation"
    elif not current_state.test_results:
        return "review"
    elif current_state.review_status == TaskStatus.COMPLETED:
        return "deployment"
    else:
        return "implementation"


def get_agent_queue(workflow_stage: str) -> List[str]:
    """Get the queue of agents for a workflow stage."""
    queues = {
        "planning": ["planner"],
        "research": ["researcher"],
        "implementation": ["coder"],
        "review": ["reviewer"],
        "deployment": ["deployer"],
    }
    return queues.get(workflow_stage, ["planner"])
