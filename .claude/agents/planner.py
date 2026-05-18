"""Planner Agent - Breaks down requirements and designs schemas."""

from pydantic import Field
from typing import List, Optional
from atomic_agents import (
    BaseIOSchema, AtomicAgent, AgentConfig, BaseTool
)
from atomic_agents.context import SystemPromptGenerator
from .shared_state import ProjectState, PlannedTask, AcceptanceCriteria
from .context_providers import ProjectStateContextProvider


# ============================================================================
# PLANNER SCHEMAS
# ============================================================================

class SchemaDef(BaseIOSchema):
    """Definition of a required schema."""
    name: str = Field(..., description="Schema name")
    purpose: str = Field(..., description="What is this schema for?")
    fields: dict = Field(..., description="Field definitions with types and descriptions")


class PlannerInput(BaseIOSchema):
    """Input to planner agent."""
    user_request: str = Field(..., description="User request or requirement")
    project_context: ProjectState = Field(..., description="Current project state")


class PlannerOutput(BaseIOSchema):
    """Output from planner agent."""
    tasks: List[PlannedTask] = Field(..., description="Planned tasks with acceptance criteria")
    schemas: List[SchemaDef] = Field(..., description="Required schemas for implementation")
    estimated_timeline: str = Field(..., description="Estimated effort/timeline")
    risks: List[str] = Field(default_factory=list, description="Identified risks")
    recommendations: List[str] = Field(default_factory=list, description="Planning recommendations")


# ============================================================================
# PLANNER AGENT FACTORY
# ============================================================================

def create_planner_agent(
    client,
    model: str = "gpt-4o-mini",
    tools: Optional[List[BaseTool]] = None
) -> AtomicAgent[PlannerInput, PlannerOutput]:
    """Create the planner agent."""

    system_prompt = SystemPromptGenerator(
        background=[
            "You are the Planner Agent - a strategic task breakdown specialist.",
            "Your role is to decompose user requirements into concrete, testable tasks.",
            "You design input/output schemas that other agents will use for implementation.",
            "You define clear acceptance criteria that the reviewer can validate against.",
        ],
        steps=[
            "1. Analyze the user request for scope, requirements, and constraints",
            "2. Break down into 2-5 concrete, independent tasks",
            "3. For each task, define clear acceptance criteria (3-5 criteria per task)",
            "4. Identify required input/output schemas for implementation",
            "5. Assess risks and dependencies between tasks",
            "6. Estimate effort levels (small, medium, large)",
        ],
        output_instructions=[
            "Each task must have 3-5 acceptance criteria",
            "Criteria must be verifiable and measurable",
            "Schema definitions must be complete and type-safe (use Python type hints)",
            "Identify dependencies: which tasks must complete before others",
            "Be specific about what 'done' looks like for each task",
        ],
    )

    agent = AtomicAgent[PlannerInput, PlannerOutput](
        config=AgentConfig(
            client=client,
            model=model,
            system_prompt_generator=system_prompt,
        )
    )

    # Register context provider for current state
    def state_provider_factory(state: ProjectState):
        return ProjectStateContextProvider(state)

    return agent


# ============================================================================
# PLANNING HELPERS
# ============================================================================

def parse_planner_output_to_state(
    planner_output: PlannerOutput,
    state: ProjectState
) -> ProjectState:
    """Convert planner output into state updates."""
    state.planned_tasks = planner_output.tasks
    state.workflow_stage = "planning"
    return state
