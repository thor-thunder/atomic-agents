"""Custom context providers for state injection into agents."""

import json
from typing import Optional
from atomic_agents.context import BaseDynamicContextProvider
from .shared_state import ProjectState


class ProjectStateContextProvider(BaseDynamicContextProvider):
    """Injects current project state into agent prompts."""

    def __init__(self, state: ProjectState):
        super().__init__("Project State Context")
        self.state = state

    def get_info(self) -> str:
        """Return formatted project state for prompt injection."""
        sections = []

        sections.append("## PROJECT OVERVIEW")
        sections.append(f"**Name:** {self.state.project_name}")
        if self.state.project_description:
            sections.append(f"**Description:** {self.state.project_description}")
        if self.state.user_request:
            sections.append(f"**User Request:** {self.state.user_request}")
        sections.append(f"**Current Stage:** {self.state.workflow_stage}")
        sections.append(f"**Current Agent:** {self.state.current_agent}")

        if self.state.planned_tasks:
            sections.append("\n## PLANNED TASKS")
            for task in self.state.planned_tasks:
                criteria_met = sum(1 for c in task.acceptance_criteria if c.verified)
                total_criteria = len(task.acceptance_criteria)
                sections.append(f"\n### {task.title} ({task.status.value})")
                sections.append(f"- **ID:** {task.task_id}")
                sections.append(f"- **Effort:** {task.estimated_effort}")
                sections.append(f"- **Acceptance Criteria:** {criteria_met}/{total_criteria} met")
                if task.dependencies:
                    sections.append(f"- **Depends On:** {', '.join(task.dependencies)}")

        if self.state.research_findings:
            sections.append("\n## RESEARCH FINDINGS")
            for finding in self.state.research_findings:
                sections.append(f"\n### {finding.topic}")
                if finding.findings:
                    sections.append("**Key Findings:**")
                    for f in finding.findings[:5]:  # Limit to 5
                        sections.append(f"- {f}")
                if finding.constraints:
                    sections.append("**Constraints:**")
                    for c in finding.constraints[:3]:
                        sections.append(f"- {c}")

        if self.state.code_changes:
            sections.append("\n## CODE CHANGES")
            sections.append(f"- **Total Files Changed:** {len(self.state.code_changes)}")
            sections.append(f"- **Implementation Status:** {self.state.implementation_status.value}")
            for change in self.state.code_changes[:5]:  # Show first 5
                sections.append(f"  - {change.file_path} ({change.change_type})")

        if self.state.test_results:
            sections.append("\n## TEST RESULTS")
            passed = sum(1 for t in self.state.test_results if t.status == "passed")
            failed = sum(1 for t in self.state.test_results if t.status == "failed")
            sections.append(f"- **Passed:** {passed}/{len(self.state.test_results)}")
            sections.append(f"- **Failed:** {failed}/{len(self.state.test_results)}")
            sections.append(f"- **Coverage:** {self.state.test_coverage}%")

        if self.state.security_audit_findings:
            sections.append("\n## SECURITY AUDIT")
            critical = sum(1 for f in self.state.security_audit_findings if f.severity == "critical")
            high = sum(1 for f in self.state.security_audit_findings if f.severity == "high")
            sections.append(f"- **Critical Issues:** {critical}")
            sections.append(f"- **High Issues:** {high}")

        if self.state.errors:
            sections.append("\n## ERRORS ENCOUNTERED")
            for error in self.state.errors[-3:]:  # Show last 3
                sections.append(f"- {error}")

        return "\n".join(sections)


class TaskContextProvider(BaseDynamicContextProvider):
    """Injects current task details."""

    def __init__(self, state: ProjectState):
        super().__init__("Current Task Context")
        self.state = state

    def get_info(self) -> str:
        """Return current task details."""
        if not self.state.planned_tasks:
            return "## TASKS\nNo tasks planned yet."

        # Find in-progress or first incomplete task
        in_progress = next(
            (t for t in self.state.planned_tasks if t.status.value == "in_progress"),
            None
        )
        current_task = in_progress or next(
            (t for t in self.state.planned_tasks if t.status.value == "pending"),
            self.state.planned_tasks[0]
        )

        sections = []
        sections.append(f"## CURRENT TASK: {current_task.title}")
        sections.append(f"**ID:** {current_task.task_id}")
        sections.append(f"**Status:** {current_task.status.value}")
        sections.append(f"**Description:** {current_task.description}")
        sections.append(f"**Effort:** {current_task.estimated_effort}")

        if current_task.acceptance_criteria:
            sections.append("\n**Acceptance Criteria:**")
            for i, criterion in enumerate(current_task.acceptance_criteria, 1):
                status = "✓" if criterion.verified else "○"
                sections.append(f"{i}. {status} {criterion.criterion}")

        if current_task.schema_definitions:
            sections.append("\n**Required Schemas:**")
            sections.append(json.dumps(current_task.schema_definitions, indent=2))

        return "\n".join(sections)


class ResearchContextProvider(BaseDynamicContextProvider):
    """Injects research findings and constraints."""

    def __init__(self, state: ProjectState):
        super().__init__("Research & Constraints Context")
        self.state = state

    def get_info(self) -> str:
        """Return research findings and constraints."""
        if not self.state.research_findings:
            return "## RESEARCH\nNo research conducted yet."

        sections = ["## RESEARCH FINDINGS & CONSTRAINTS"]

        for finding in self.state.research_findings:
            sections.append(f"\n### {finding.topic}")

            if finding.findings:
                sections.append("**Key Points:**")
                for item in finding.findings:
                    sections.append(f"- {item}")

            if finding.constraints:
                sections.append("**Constraints:**")
                for constraint in finding.constraints:
                    sections.append(f"- {constraint}")

            if finding.recommendations:
                sections.append("**Recommendations:**")
                for rec in finding.recommendations:
                    sections.append(f"- {rec}")

            if finding.sources:
                sections.append("**Sources:**")
                for source in finding.sources[:3]:
                    sections.append(f"- {source}")

        return "\n".join(sections)


class CodeContextProvider(BaseDynamicContextProvider):
    """Injects code changes and implementation status."""

    def __init__(self, state: ProjectState):
        super().__init__("Code & Implementation Context")
        self.state = state

    def get_info(self) -> str:
        """Return code changes and status."""
        if not self.state.code_changes:
            return "## CODE\nNo code changes yet."

        sections = ["## CODE CHANGES & STATUS"]
        sections.append(f"**Implementation Status:** {self.state.implementation_status.value}")
        sections.append(f"**Files Modified:** {len(self.state.code_changes)}")

        sections.append("\n**Changes:**")
        for change in self.state.code_changes:
            sections.append(f"\n- **File:** {change.file_path}")
            sections.append(f"  - **Type:** {change.change_type}")
            sections.append(f"  - **Description:** {change.description}")
            if change.tdd_test_first:
                sections.append(f"  - **TDD:** Tests written first ✓")
            if change.tests_added:
                sections.append(f"  - **Tests:** {', '.join(change.tests_added)}")

        return "\n".join(sections)


class ReviewContextProvider(BaseDynamicContextProvider):
    """Injects review results, tests, and quality metrics."""

    def __init__(self, state: ProjectState):
        super().__init__("Review & Quality Context")
        self.state = state

    def get_info(self) -> str:
        """Return review and quality information."""
        sections = ["## QUALITY & REVIEW METRICS"]
        sections.append(f"**Review Status:** {self.state.review_status.value}")

        if self.state.test_results:
            sections.append(f"\n**Test Results:** ({len(self.state.test_results)} total)")
            passed = sum(1 for t in self.state.test_results if t.status == "passed")
            failed = sum(1 for t in self.state.test_results if t.status == "failed")
            sections.append(f"- Passed: {passed}")
            sections.append(f"- Failed: {failed}")
            sections.append(f"- Coverage: {self.state.test_coverage}%")
            sections.append(f"- Quality Score: {self.state.code_quality_score}/100")

        if self.state.security_audit_findings:
            sections.append(f"\n**Security Audit:** ({len(self.state.security_audit_findings)} issues)")
            critical = sum(1 for f in self.state.security_audit_findings if f.severity == "critical")
            high = sum(1 for f in self.state.security_audit_findings if f.severity == "high")
            medium = sum(1 for f in self.state.security_audit_findings if f.severity == "medium")
            sections.append(f"- Critical: {critical}")
            sections.append(f"- High: {high}")
            sections.append(f"- Medium: {medium}")

            open_issues = [f for f in self.state.security_audit_findings if f.status == "open"]
            if open_issues:
                sections.append("\n**Open Security Issues:**")
                for issue in open_issues[:5]:
                    sections.append(f"- [{issue.severity.upper()}] {issue.category}: {issue.description}")

        return "\n".join(sections)
