"""
Linting and formatting tools for agents.

Provides tools for code quality checks, formatting, and style enforcement.
"""
import subprocess
from typing import Dict, Any
from pathlib import Path

from .base import BaseTool, ToolResult


class FormatCodeTool(BaseTool):
    """Format code using Black (Python)."""

    name = "format_code"
    description = "Format Python code using Black formatter"

    parameters_schema = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to file or directory to format (relative to project root). Leave empty to format all."
            },
            "check_only": {
                "type": "boolean",
                "description": "Only check formatting without making changes",
                "default": False
            }
        },
        "required": []
    }

    async def execute(self, arguments: Dict[str, Any]) -> ToolResult:
        """Execute code formatting."""
        file_path = arguments.get("file_path", "")
        check_only = arguments.get("check_only", False)

        try:
            project_path = self.agent.project.local_path
            if not project_path:
                return ToolResult(
                    success=False,
                    error="Project path not set"
                )

            # Build black command
            cmd = ["black"]

            if check_only:
                cmd.append("--check")

            if file_path:
                cmd.append(str(Path(project_path) / file_path))
            else:
                cmd.append(".")

            # Run black
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120
            )

            formatted = result.returncode == 0
            output = result.stdout + result.stderr

            # Count reformatted files
            reformatted_count = output.count("reformatted")
            unchanged_count = output.count("left unchanged")

            return ToolResult(
                success=True,
                result={
                    "formatted": formatted,
                    "check_only": check_only,
                    "files_reformatted": reformatted_count,
                    "files_unchanged": unchanged_count,
                    "output": output
                }
            )

        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                error="Formatting timed out"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Failed to format code: {str(e)}"
            )


class RunLinterTool(BaseTool):
    """Run linter (Ruff) on code."""

    name = "run_linter"
    description = "Run Ruff linter to check code quality and style issues"

    parameters_schema = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to file or directory to lint (relative to project root). Leave empty for all."
            },
            "fix": {
                "type": "boolean",
                "description": "Automatically fix issues when possible",
                "default": False
            }
        },
        "required": []
    }

    async def execute(self, arguments: Dict[str, Any]) -> ToolResult:
        """Execute linting."""
        file_path = arguments.get("file_path", "")
        fix = arguments.get("fix", False)

        try:
            project_path = self.agent.project.local_path
            if not project_path:
                return ToolResult(
                    success=False,
                    error="Project path not set"
                )

            # Build ruff command
            cmd = ["ruff", "check"]

            if fix:
                cmd.append("--fix")

            if file_path:
                cmd.append(str(Path(project_path) / file_path))
            else:
                cmd.append(".")

            # Run ruff
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120
            )

            # Ruff returns 0 if no issues, 1 if issues found
            has_issues = result.returncode != 0
            output = result.stdout + result.stderr

            # Parse issues
            issues = self._parse_ruff_output(output)

            return ToolResult(
                success=True,
                result={
                    "has_issues": has_issues,
                    "fixed": fix,
                    "issue_count": len(issues),
                    "issues": issues,
                    "output": output
                }
            )

        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                error="Linting timed out"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Failed to run linter: {str(e)}"
            )

    def _parse_ruff_output(self, output: str) -> list:
        """Parse Ruff output to extract issues."""
        issues = []

        for line in output.split('\n'):
            # Ruff format: file.py:line:col: CODE message
            if '.py:' in line and ':' in line:
                parts = line.split(':', 3)
                if len(parts) >= 4:
                    try:
                        issues.append({
                            "file": parts[0],
                            "line": int(parts[1]),
                            "column": int(parts[2]),
                            "message": parts[3].strip()
                        })
                    except:
                        pass

        return issues


class TypeCheckTool(BaseTool):
    """Run type checker (mypy) on code."""

    name = "type_check"
    description = "Run mypy type checker to find type errors"

    parameters_schema = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to file or directory to type check"
            }
        },
        "required": []
    }

    async def execute(self, arguments: Dict[str, Any]) -> ToolResult:
        """Execute type checking."""
        file_path = arguments.get("file_path", "")

        try:
            project_path = self.agent.project.local_path
            if not project_path:
                return ToolResult(
                    success=False,
                    error="Project path not set"
                )

            # Build mypy command
            cmd = ["mypy"]

            if file_path:
                cmd.append(str(Path(project_path) / file_path))
            else:
                cmd.append(".")

            # Run mypy
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=180
            )

            # mypy returns 0 if no errors
            has_errors = result.returncode != 0
            output = result.stdout + result.stderr

            # Parse errors
            errors = self._parse_mypy_output(output)

            return ToolResult(
                success=True,
                result={
                    "has_errors": has_errors,
                    "error_count": len(errors),
                    "errors": errors,
                    "output": output
                }
            )

        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                error="Type checking timed out"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Failed to run type checker: {str(e)}"
            )

    def _parse_mypy_output(self, output: str) -> list:
        """Parse mypy output to extract errors."""
        errors = []

        for line in output.split('\n'):
            # mypy format: file.py:line: error: message
            if '.py:' in line and 'error:' in line:
                parts = line.split(':', 2)
                if len(parts) >= 3:
                    try:
                        error_part = parts[2].strip()
                        if error_part.startswith('error:'):
                            errors.append({
                                "file": parts[0],
                                "line": int(parts[1]),
                                "message": error_part.replace('error:', '').strip()
                            })
                    except:
                        pass

        return errors


class SecurityCheckTool(BaseTool):
    """Run security checks using bandit."""

    name = "security_check"
    description = "Run Bandit security checker to find security issues in Python code"

    parameters_schema = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to file or directory to check"
            },
            "severity": {
                "type": "string",
                "enum": ["all", "low", "medium", "high"],
                "description": "Minimum severity level to report",
                "default": "medium"
            }
        },
        "required": []
    }

    async def execute(self, arguments: Dict[str, Any]) -> ToolResult:
        """Execute security check."""
        file_path = arguments.get("file_path", "")
        severity = arguments.get("severity", "medium")

        try:
            project_path = self.agent.project.local_path
            if not project_path:
                return ToolResult(
                    success=False,
                    error="Project path not set"
                )

            # Build bandit command
            cmd = ["bandit", "-r"]

            if severity != "all":
                severity_map = {"low": "l", "medium": "m", "high": "h"}
                cmd.extend(["-ll", "-ii"])  # Set severity threshold

            if file_path:
                cmd.append(str(Path(project_path) / file_path))
            else:
                cmd.append(".")

            # Add JSON output
            cmd.extend(["-f", "json"])

            # Run bandit
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120
            )

            output = result.stdout

            # Parse JSON output
            try:
                import json
                data = json.loads(output)
                issues = data.get('results', [])

                formatted_issues = [
                    {
                        "file": issue['filename'],
                        "line": issue['line_number'],
                        "severity": issue['issue_severity'],
                        "confidence": issue['issue_confidence'],
                        "message": issue['issue_text']
                    }
                    for issue in issues
                ]

                return ToolResult(
                    success=True,
                    result={
                        "has_issues": len(issues) > 0,
                        "issue_count": len(issues),
                        "issues": formatted_issues
                    }
                )
            except:
                # Fallback if JSON parsing fails
                return ToolResult(
                    success=True,
                    result={
                        "has_issues": result.returncode != 0,
                        "output": output
                    }
                )

        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                error="Security check timed out"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Failed to run security check: {str(e)}"
            )
