"""Coder/Implementer Agent - Writes code following TDD principles."""

from pydantic import Field
from typing import List, Optional
from atomic_agents import (
    BaseIOSchema, AtomicAgent, AgentConfig, BaseTool
)
from atomic_agents.context import SystemPromptGenerator
from .shared_state import ProjectState, CodeChange
from .context_providers import (
    ProjectStateContextProvider,
    TaskContextProvider,
    ResearchContextProvider
)


# ============================================================================
# CODER SCHEMAS
# ============================================================================

class CoderInput(BaseIOSchema):
    """Input to coder agent."""
    implementation_task: str = Field(..., description="What to implement")
    project_context: ProjectState = Field(..., description="Current project state")
    schemas: dict = Field(
        default_factory=dict,
        description="Schema definitions from planner"
    )
    constraints: List[str] = Field(
        default_factory=list,
        description="Implementation constraints from research"
    )


class TestCase(BaseIOSchema):
    """Definition of a test case."""
    test_name: str = Field(..., description="Name of the test")
    test_code: str = Field(..., description="Test code (pytest format)")
    purpose: str = Field(..., description="What this test validates")


class CoderOutput(BaseIOSchema):
    """Output from coder agent."""
    code_changes: List[CodeChange] = Field(..., description="Files changed or created")
    test_cases: List[TestCase] = Field(..., description="Test cases written (TDD)")
    implementation_notes: str = Field(default="", description="Implementation notes")
    decisions_made: List[str] = Field(
        default_factory=list,
        description="Key decisions in implementation"
    )
    potential_issues: List[str] = Field(
        default_factory=list,
        description="Known issues or edge cases to consider"
    )
    code_structure: str = Field(
        default="",
        description="Summary of code organization"
    )


# ============================================================================
# CODER AGENT FACTORY
# ============================================================================

def create_coder_agent(
    client,
    model: str = "gpt-4o-mini",
    tools: Optional[List[BaseTool]] = None
) -> AtomicAgent[CoderInput, CoderOutput]:
    """Create the coder/implementer agent."""

    system_prompt = SystemPromptGenerator(
        background=[
            "You are the Coder Agent - the implementation specialist.",
            "Your role is to write high-quality, production-ready code.",
            "You follow Test-Driven Development (TDD): tests first, then implementation.",
            "You follow the atomic-agents framework patterns and best practices.",
            "You write code that is type-safe, well-structured, and maintainable.",
        ],
        steps=[
            "1. Understand the implementation task and requirements",
            "2. Review the planned tasks and acceptance criteria",
            "3. Study the research findings and constraints",
            "4. Write comprehensive test cases FIRST (TDD approach)",
            "5. Implement code that makes the tests pass",
            "6. Ensure code follows project style and patterns",
            "7. Document key decisions and potential issues",
        ],
        output_instructions=[
            "CRITICAL: Write tests BEFORE implementation (TDD pattern)",
            "Use pytest format for tests with clear descriptions",
            "Each test should validate one acceptance criterion",
            "Include docstrings for all functions and classes",
            "Use type hints throughout (Pydantic for schemas)",
            "Follow atomic-agents patterns: BaseIOSchema, BaseTool, AtomicAgent",
            "Add comments only for non-obvious WHY decisions",
            "List any edge cases or known limitations",
        ],
    )

    agent = AtomicAgent[CoderInput, CoderOutput](
        config=AgentConfig(
            client=client,
            model=model,
            system_prompt_generator=system_prompt,
        )
    )

    return agent


# ============================================================================
# CODER HELPERS
# ============================================================================

def parse_coder_output_to_state(
    coder_output: CoderOutput,
    state: ProjectState
) -> ProjectState:
    """Convert coder output into state updates."""
    state.code_changes = coder_output.code_changes
    state.implementation_status = state.implementation_status  # Mark as in progress
    state.workflow_stage = "implementation"
    return state
