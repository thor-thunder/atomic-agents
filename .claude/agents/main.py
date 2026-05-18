"""Main orchestration runner for the 6-agent atomic team."""

import json
from pathlib import Path
from typing import Optional
import os
from dotenv import load_dotenv

from atomic_agents import AtomicAgent
from .shared_state import ProjectState
from .orchestrator import create_orchestrator_agent, OrchestratorInput, OrchestratorOutput
from .planner import create_planner_agent, PlannerInput, PlannerOutput
from .researcher import create_researcher_agent, ResearcherInput, ResearcherOutput
from .coder import create_coder_agent, CoderInput, CoderOutput
from .reviewer import create_reviewer_agent, ReviewerInput, ReviewerOutput
from .deployer import create_deployer_agent, DeployerInput, DeployerOutput


# Load environment variables
load_dotenv()


class AgentTeam:
    """Manages the 6-agent team orchestration."""

    def __init__(self, provider: str = "openai", model: Optional[str] = None, verbose: bool = False):
        """Initialize the agent team.

        Args:
            provider: LLM provider (openai, anthropic, groq, etc.)
            model: Model name (e.g., gpt-4o-mini, claude-3-5-sonnet, llama-3.1-70b)
            verbose: Enable detailed logging
        """
        self.provider = provider
        self.verbose = verbose

        # Set default models per provider
        self.models = {
            "openai": model or "gpt-4o-mini",
            "anthropic": model or "claude-3-5-sonnet-20241022",
            "groq": model or "mixtral-8x7b-32768",
        }

        self.model = self.models.get(provider, model or "gpt-4o-mini")

        # Initialize LLM client
        self.client = self._initialize_client()

        # Create agents
        self.orchestrator = create_orchestrator_agent(self.client, self.model)
        self.planner = create_planner_agent(self.client, self.model)
        self.researcher = create_researcher_agent(self.client, self.model)
        self.coder = create_coder_agent(self.client, self.model)
        self.reviewer = create_reviewer_agent(self.client, self.model)
        self.deployer = create_deployer_agent(self.client, self.model)

        self.agents = {
            "orchestrator": self.orchestrator,
            "planner": self.planner,
            "researcher": self.researcher,
            "coder": self.coder,
            "reviewer": self.reviewer,
            "deployer": self.deployer,
        }

    def _initialize_client(self):
        """Initialize LLM client based on provider."""
        if self.provider == "openai":
            import instructor
            from openai import OpenAI
            return instructor.from_openai(
                OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            )
        elif self.provider == "anthropic":
            import instructor
            from anthropic import Anthropic
            return instructor.from_anthropic(
                Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            )
        elif self.provider == "groq":
            import instructor
            from groq import Groq
            return instructor.from_groq(
                Groq(api_key=os.getenv("GROQ_API_KEY"))
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def run_workflow(
        self,
        user_request: str,
        project_name: str = "atomic-project",
        project_description: str = "",
    ) -> ProjectState:
        """Run a complete workflow from request to deployment.

        Args:
            user_request: The user's request or feature description
            project_name: Name of the project
            project_description: Project description

        Returns:
            Final ProjectState with all results
        """
        # Initialize shared state
        state = ProjectState(
            project_name=project_name,
            project_description=project_description,
            user_request=user_request,
        )

        if self.verbose:
            print(f"\n🚀 Starting workflow: {user_request}")
            print(f"   Project: {project_name}")

        # Orchestrator coordinates the workflow
        stage = "planning"
        max_iterations = 6  # Prevent infinite loops

        for iteration in range(max_iterations):
            if self.verbose:
                print(f"\n📍 Stage {iteration + 1}: {stage}")

            if stage == "planning":
                state = self._run_planner(state)
                stage = "research"

            elif stage == "research":
                state = self._run_researcher(state)
                stage = "implementation"

            elif stage == "implementation":
                state = self._run_coder(state)
                stage = "review"

            elif stage == "review":
                state = self._run_reviewer(state)
                # Check if review passed
                if state.review_status.value == "completed":
                    stage = "deployment"
                else:
                    if self.verbose:
                        print("   ❌ Review failed. Check blockers.")
                    break

            elif stage == "deployment":
                state = self._run_deployer(state)
                if self.verbose:
                    print("   ✅ Deployment complete!")
                break

        if self.verbose:
            print(f"\n🎉 Workflow complete!")
            self._print_summary(state)

        return state

    def _run_planner(self, state: ProjectState) -> ProjectState:
        """Run the planner agent."""
        from .planner import parse_planner_output_to_state

        if self.verbose:
            print("   Planning tasks and schemas...")

        input_obj = PlannerInput(
            user_request=state.user_request,
            project_context=state,
        )

        output = self.planner.run(input_obj)
        state = parse_planner_output_to_state(output, state)

        if self.verbose:
            print(f"   ✓ Planned {len(output.tasks)} tasks")

        return state

    def _run_researcher(self, state: ProjectState) -> ProjectState:
        """Run the researcher agent."""
        from .researcher import parse_researcher_output_to_state

        if self.verbose:
            print("   Researching requirements and constraints...")

        input_obj = ResearcherInput(
            research_topic=f"Requirements for: {state.user_request}",
            project_context=state,
        )

        output = self.researcher.run(input_obj)
        state = parse_researcher_output_to_state(output, state)

        if self.verbose:
            print(f"   ✓ Research findings: {len(output.findings.findings)} key points")

        return state

    def _run_coder(self, state: ProjectState) -> ProjectState:
        """Run the coder agent."""
        from .coder import parse_coder_output_to_state

        if self.verbose:
            print("   Writing code and tests...")

        input_obj = CoderInput(
            implementation_task=state.user_request,
            project_context=state,
        )

        output = self.coder.run(input_obj)
        state = parse_coder_output_to_state(output, state)

        if self.verbose:
            print(f"   ✓ Code changes: {len(output.code_changes)} files")
            print(f"   ✓ Test cases: {len(output.test_cases)} tests (TDD)")

        return state

    def _run_reviewer(self, state: ProjectState) -> ProjectState:
        """Run the reviewer agent."""
        from .reviewer import parse_reviewer_output_to_state

        if self.verbose:
            print("   Reviewing code, running tests, security audit...")

        input_obj = ReviewerInput(
            code_to_review="[Code review based on state]",
            project_context=state,
        )

        output = self.reviewer.run(input_obj)
        state = parse_reviewer_output_to_state(output, state)

        if self.verbose:
            print(f"   ✓ Tests: {len(output.test_results)} (pass: {output.overall_test_pass})")
            print(f"   ✓ Coverage: {output.test_coverage}%")
            print(f"   ✓ Quality Score: {output.quality_score}/100")
            if output.security_findings:
                print(f"   ⚠️  Security: {len(output.security_findings)} findings")

        return state

    def _run_deployer(self, state: ProjectState) -> ProjectState:
        """Run the deployer agent."""
        from .deployer import parse_deployer_output_to_state

        if self.verbose:
            print("   Deploying and optimizing...")

        input_obj = DeployerInput(
            deployment_target="production",
            project_context=state,
        )

        output = self.deployer.run(input_obj)
        state = parse_deployer_output_to_state(output, state)

        if self.verbose:
            print(f"   ✓ Deployment: {output.deployment_successful}")
            print(f"   ✓ Documentation: {len(output.generated_documentation)} assets")

        return state

    def _print_summary(self, state: ProjectState):
        """Print workflow summary."""
        print("\n" + "=" * 60)
        print(f"PROJECT: {state.project_name}")
        print("=" * 60)
        print(f"Tasks Planned:    {len(state.planned_tasks)}")
        print(f"Code Files:       {len(state.code_changes)}")
        print(f"Tests Written:    {sum(1 for c in state.code_changes for t in c.tests_added)}")
        print(f"Test Coverage:    {state.test_coverage}%")
        print(f"Code Quality:     {state.code_quality_score}/100")
        print(f"Security Issues:  {len(state.security_audit_findings)}")
        print(f"Deployment:       {state.deployment_status.value}")
        print("=" * 60)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Atomic Agents 6-Team System"
    )
    parser.add_argument("--request", required=True, help="User request/task")
    parser.add_argument("--project", default="atomic-project", help="Project name")
    parser.add_argument("--provider", default="openai", help="LLM provider")
    parser.add_argument("--model", help="Model name (optional)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Initialize team and run workflow
    team = AgentTeam(provider=args.provider, model=args.model, verbose=args.verbose)
    state = team.run_workflow(
        user_request=args.request,
        project_name=args.project,
    )

    # Save final state
    output_file = Path(f"{args.project}_state.json")
    with open(output_file, "w") as f:
        json.dump(state.dict(), f, indent=2, default=str)

    print(f"\n💾 State saved to: {output_file}")


if __name__ == "__main__":
    main()
