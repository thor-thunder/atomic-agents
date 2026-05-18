"""Shared tools for agent team - safe file operations, analysis, and execution."""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import Field
from atomic_agents import BaseTool, BaseIOSchema, BaseToolConfig


# ============================================================================
# INPUT/OUTPUT SCHEMAS
# ============================================================================

class FileReadInput(BaseIOSchema):
    """Input for reading a file."""
    file_path: str = Field(..., description="Path to file to read")
    max_lines: Optional[int] = Field(None, description="Maximum lines to read (None=all)")


class FileReadOutput(BaseIOSchema):
    """Output from reading a file."""
    content: str = Field(..., description="File content")
    lines_read: int = Field(..., description="Number of lines read")
    truncated: bool = Field(False, description="Whether output was truncated")


class FileWriteInput(BaseIOSchema):
    """Input for writing a file."""
    file_path: str = Field(..., description="Path to file to write")
    content: str = Field(..., description="Content to write")
    create_dirs: bool = Field(True, description="Create parent directories if needed")
    mode: str = Field("w", description="Write mode: 'w' (overwrite) or 'a' (append)")


class FileWriteOutput(BaseIOSchema):
    """Output from writing a file."""
    success: bool = Field(..., description="Whether write succeeded")
    message: str = Field(..., description="Status message")
    bytes_written: int = Field(..., description="Bytes written")


class DirectoryListInput(BaseIOSchema):
    """Input for listing directory."""
    directory: str = Field(..., description="Directory path")
    pattern: Optional[str] = Field(None, description="Glob pattern to filter (e.g., '*.py')")
    recursive: bool = Field(False, description="List recursively")


class DirectoryListOutput(BaseIOSchema):
    """Output from directory listing."""
    files: List[str] = Field(..., description="List of files found")
    count: int = Field(..., description="Total files found")
    directory: str = Field(..., description="Directory listed")


class ShellExecuteInput(BaseIOSchema):
    """Input for executing a shell command."""
    command: str = Field(..., description="Command to execute")
    working_dir: Optional[str] = Field(None, description="Working directory")
    timeout_seconds: int = Field(30, description="Command timeout in seconds")


class ShellExecuteOutput(BaseIOSchema):
    """Output from shell execution."""
    returncode: int = Field(..., description="Return code (0=success)")
    stdout: str = Field(..., description="Standard output")
    stderr: str = Field(..., description="Standard error")
    command: str = Field(..., description="Command that was executed")


class CodeAnalysisInput(BaseIOSchema):
    """Input for analyzing code."""
    file_path: str = Field(..., description="Path to Python file to analyze")


class CodeAnalysisOutput(BaseIOSchema):
    """Output from code analysis."""
    imports: List[str] = Field(..., description="Imported modules")
    classes: List[str] = Field(..., description="Classes defined")
    functions: List[str] = Field(..., description="Functions defined")
    dependencies: List[str] = Field(..., description="External dependencies")
    issues: List[str] = Field(..., description="Potential issues found")


# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

class FileReadTool(BaseTool[FileReadInput, FileReadOutput]):
    """Reads file content with optional line limit."""

    def __init__(self, config: BaseToolConfig = BaseToolConfig()):
        super().__init__(config)
        self.config.title = "Read File"
        self.config.description = "Read contents of a file"

    def run(self, params: FileReadInput) -> FileReadOutput:
        """Execute file read."""
        try:
            path = Path(params.file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {params.file_path}")

            with open(path, "r", encoding="utf-8") as f:
                if params.max_lines:
                    lines = [f.readline() for _ in range(params.max_lines)]
                    content = "".join(lines)
                    truncated = len(lines) == params.max_lines
                else:
                    content = f.read()
                    truncated = False

            return FileReadOutput(
                content=content,
                lines_read=len(content.splitlines()),
                truncated=truncated
            )
        except Exception as e:
            raise ValueError(f"Failed to read file: {str(e)}")


class FileWriteTool(BaseTool[FileWriteInput, FileWriteOutput]):
    """Writes content to a file."""

    def __init__(self, config: BaseToolConfig = BaseToolConfig()):
        super().__init__(config)
        self.config.title = "Write File"
        self.config.description = "Write or append content to a file"

    def run(self, params: FileWriteInput) -> FileWriteOutput:
        """Execute file write."""
        try:
            path = Path(params.file_path)

            if params.create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)

            mode = "a" if params.mode == "a" else "w"
            with open(path, mode, encoding="utf-8") as f:
                bytes_written = f.write(params.content)

            return FileWriteOutput(
                success=True,
                message=f"Wrote to {params.file_path}",
                bytes_written=bytes_written
            )
        except Exception as e:
            raise ValueError(f"Failed to write file: {str(e)}")


class DirectoryListTool(BaseTool[DirectoryListInput, DirectoryListOutput]):
    """Lists files in a directory."""

    def __init__(self, config: BaseToolConfig = BaseToolConfig()):
        super().__init__(config)
        self.config.title = "List Directory"
        self.config.description = "List files in a directory"

    def run(self, params: DirectoryListInput) -> DirectoryListOutput:
        """Execute directory listing."""
        try:
            path = Path(params.directory)
            if not path.exists():
                raise FileNotFoundError(f"Directory not found: {params.directory}")

            if params.recursive:
                pattern = f"**/{params.pattern}" if params.pattern else "**/*"
                files = [str(p.relative_to(path)) for p in path.glob(pattern) if p.is_file()]
            else:
                pattern = params.pattern or "*"
                files = [p.name for p in path.glob(pattern) if p.is_file()]

            files.sort()
            return DirectoryListOutput(
                files=files,
                count=len(files),
                directory=params.directory
            )
        except Exception as e:
            raise ValueError(f"Failed to list directory: {str(e)}")


class ShellExecuteTool(BaseTool[ShellExecuteInput, ShellExecuteOutput]):
    """Executes shell commands (with safety limits)."""

    ALLOWED_COMMANDS = [
        "python", "pytest", "pip", "git", "ls", "pwd", "cat",
        "find", "grep", "curl", "npm", "node", "docker"
    ]

    def __init__(self, config: BaseToolConfig = BaseToolConfig()):
        super().__init__(config)
        self.config.title = "Execute Shell Command"
        self.config.description = "Execute a shell command safely"

    def run(self, params: ShellExecuteInput) -> ShellExecuteOutput:
        """Execute shell command with safety checks."""
        try:
            # Security: Check if command starts with allowed command
            cmd_base = params.command.split()[0].lower()
            if not any(cmd_base.endswith(allowed) for allowed in self.ALLOWED_COMMANDS):
                raise ValueError(f"Command not allowed: {cmd_base}")

            # Prevent dangerous patterns
            dangerous_patterns = ["rm -rf", "sudo", "chmod", "useradd", ">"]
            if any(pattern in params.command for pattern in dangerous_patterns):
                raise ValueError("Dangerous command pattern detected")

            result = subprocess.run(
                params.command,
                shell=True,
                cwd=params.working_dir or os.getcwd(),
                capture_output=True,
                text=True,
                timeout=params.timeout_seconds
            )

            return ShellExecuteOutput(
                returncode=result.returncode,
                stdout=result.stdout[:5000],  # Limit output
                stderr=result.stderr[:5000],
                command=params.command
            )
        except subprocess.TimeoutExpired:
            raise ValueError(f"Command timed out after {params.timeout_seconds}s")
        except Exception as e:
            raise ValueError(f"Failed to execute command: {str(e)}")


class CodeAnalysisTool(BaseTool[CodeAnalysisInput, CodeAnalysisOutput]):
    """Analyzes Python code structure."""

    def __init__(self, config: BaseToolConfig = BaseToolConfig()):
        super().__init__(config)
        self.config.title = "Analyze Code"
        self.config.description = "Analyze Python code structure and dependencies"

    def run(self, params: CodeAnalysisInput) -> CodeAnalysisOutput:
        """Analyze Python code."""
        try:
            import ast
            import re

            path = Path(params.file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {params.file_path}")

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            imports = []
            classes = []
            functions = []
            issues = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    functions.append(node.name)

            # Check for common issues
            if "TODO" in content or "FIXME" in content:
                issues.append("Contains TODO/FIXME comments")
            if "except:" in content:
                issues.append("Bare except clause found")
            if content.count("\n") > 500:
                issues.append("File is quite long (>500 lines)")

            return CodeAnalysisOutput(
                imports=list(set(imports)),
                classes=classes,
                functions=functions,
                dependencies=self._extract_dependencies(imports),
                issues=issues
            )
        except Exception as e:
            raise ValueError(f"Failed to analyze code: {str(e)}")

    @staticmethod
    def _extract_dependencies(imports: List[str]) -> List[str]:
        """Extract third-party dependencies from imports."""
        stdlib = {
            "os", "sys", "json", "re", "datetime", "typing", "pathlib",
            "subprocess", "ast", "collections", "itertools", "functools"
        }
        return [imp for imp in imports if imp not in stdlib and "." not in imp]


# ============================================================================
# TOOL FACTORY
# ============================================================================

def create_agent_tools() -> Dict[str, BaseTool]:
    """Create all available tools for agents."""
    return {
        "read_file": FileReadTool(),
        "write_file": FileWriteTool(),
        "list_directory": DirectoryListTool(),
        "execute_shell": ShellExecuteTool(),
        "analyze_code": CodeAnalysisTool(),
    }
