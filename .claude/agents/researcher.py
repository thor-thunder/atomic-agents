"""Researcher/Context Agent - Gathers documentation and analyzes requirements."""

from pydantic import Field
from typing import List, Optional
from atomic_agents import (
    BaseIOSchema, AtomicAgent, AgentConfig, BaseTool
)
from atomic_agents.context import SystemPromptGenerator
from .shared_state import ProjectState, ResearchFindings
from .context_providers import ProjectStateContextProvider, TaskContextProvider


# ============================================================================
# RESEARCHER SCHEMAS
# ============================================================================

class ResearcherInput(BaseIOSchema):
    """Input to researcher agent."""
    research_topic: str = Field(..., description="What to research")
    project_context: ProjectState = Field(..., description="Current project state")
    sources_to_check: List[str] = Field(
        default_factory=list,
        description="Specific files or documentation to review"
    )


class ResearcherOutput(BaseIOSchema):
    """Output from researcher agent."""
    findings: ResearchFindings = Field(..., description="Research findings and analysis")
    documentation_review: dict = Field(
        default_factory=dict,
        description="Summary of reviewed documentation"
    )
    architecture_notes: str = Field(
        default="",
        description="Notes on relevant architecture from codebase"
    )
    integration_points: List[str] = Field(
        default_factory=list,
        description="How this work integrates with existing code"
    )
    next_steps: List[str] = Field(
        default_factory=list,
        description="Recommended next steps based on research"
    )


# ============================================================================
# RESEARCHER AGENT FACTORY
# ============================================================================

def create_researcher_agent(
    client,
    model: str = "gpt-4o-mini",
    tools: Optional[List[BaseTool]] = None
) -> AtomicAgent[ResearcherInput, ResearcherOutput]:
    """Create the researcher agent."""

    system_prompt = SystemPromptGenerator(
        background=[
            "You are the Researcher Agent - a context and documentation specialist.",
            "Your role is to gather all necessary information before implementation begins.",
            "You analyze requirements, read relevant documentation, and identify constraints.",
            "You bridge the gap between what users want and what the codebase supports.",
        ],
        steps=[
            "1. Understand the research topic and project context",
            "2. Identify what documentation, examples, or code needs review",
            "3. Analyze relevant framework patterns (e.g., from atomic-agents examples)",
            "4. Document constraints: API limitations, compatibility issues, architecture rules",
            "5. Map integration points: how does this fit with existing code?",
            "6. Compile findings into actionable recommendations",
        ],
        output_instructions=[
            "Key findings should be concrete and specific",
            "Constraints must be documented with their source/reason",
            "Always note which files or documentation you reviewed",
            "Provide architectural context for the implementation team",
            "Identify potential blockers early",
        ],
    )

    agent = AtomicAgent[ResearcherInput, ResearcherOutput](
        config=AgentConfig(
            client=client,
            model=model,
            system_prompt_generator=system_prompt,
        )
    )

    return agent


# ============================================================================
# RESEARCH HELPERS
# ============================================================================

def parse_researcher_output_to_state(
    researcher_output: ResearcherOutput,
    state: ProjectState
) -> ProjectState:
    """Convert researcher output into state updates."""
    state.research_findings.append(researcher_output.findings)
    state.workflow_stage = "research"
    return state
