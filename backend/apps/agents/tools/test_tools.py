"""
Testing tools for agents.

Provides tools for running tests, generating coverage reports, and creating test files.
"""
import subprocess
import json
from typing import Dict, Any
from pathlib import Path

from .base import BaseTool, ToolResult


class RunTestsTool(BaseTool):
    """Run tests using pytest."""

    name = "run_tests"
    description = "Run tests for the project or specific test file/function"

    parameters_schema = {
        "type": "object",
        "properties": {
            "test_path": {
                "type": "string",
                "description": "Path to test file or directory (relative to project root). Leave empty to run all tests.",
                "default": ""
            },
            "test_name": {
                "type": "string",
                "description": "Specific test function/class name to run",
                "default": ""
            },
            "verbose": {
                "type": "boolean",
                "description": "Show verbose output",
                "default": True
            },
            "coverage": {
                "type": "boolean",
                "description": "Generate coverage report",
                "default": False
            }
        },
        "required": []
    }

    async def execute(self, arguments: Dict[str, Any]) -> ToolResult:
        """Execute tests."""
        test_path = arguments.get("test_path", "")
        test_name = arguments.get("test_name", "")
        verbose = arguments.get("verbose", True)
        coverage = arguments.get("coverage", False)

        try:
            project_path = self.agent.project.local_path
            if not project_path:
                return ToolResult(
                    success=False,
                    error="Project path not set"
                )

            # Build pytest command
            cmd = ["pytest"]

            if test_path:
                full_path = str(Path(project_path) / test_path)
                if test_name:
                    full_path += f"::{test_name}"
                cmd.append(full_path)

            if verbose:
                cmd.append("-v")

            if coverage:
                cmd.extend(["--cov", "--cov-report=term-missing"])

            # Add JSON output for parsing
            cmd.extend(["--json-report", "--json-report-omit", "log"])

            # Run tests
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes
            )

            # Parse output
            passed = result.returncode == 0
            output = result.stdout + result.stderr

            # Try to extract summary
            summary = self._parse_pytest_output(output)

            return ToolResult(
                success=True,
                result={
                    "passed": passed,
                    "exit_code": result.returncode,
                    "output": output,
                    "summary": summary
                }
            )

        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                error="Tests timed out after 5 minutes"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Failed to run tests: {str(e)}"
            )

    def _parse_pytest_output(self, output: str) -> Dict[str, Any]:
        """Parse pytest output to extract summary."""
        summary = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0
        }

        # Look for summary line like "5 passed, 2 failed in 1.23s"
        for line in output.split('\n'):
            if 'passed' in line or 'failed' in line:
                if 'passed' in line:
                    try:
                        passed = int(line.split('passed')[0].strip().split()[-1])
                        summary['passed'] = passed
                    except:
                        pass
                if 'failed' in line:
                    try:
                        failed = int(line.split('failed')[0].strip().split()[-1])
                        summary['failed'] = failed
                    except:
                        pass
                if 'skipped' in line:
                    try:
                        skipped = int(line.split('skipped')[0].strip().split()[-1])
                        summary['skipped'] = skipped
                    except:
                        pass

        summary['total'] = summary['passed'] + summary['failed'] + summary['skipped']
        return summary


class RunCoverageTool(BaseTool):
    """Generate test coverage report."""

    name = "run_coverage"
    description = "Generate comprehensive test coverage report"

    parameters_schema = {
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "enum": ["term", "html", "json", "xml"],
                "description": "Output format for coverage report",
                "default": "term"
            }
        },
        "required": []
    }

    async def execute(self, arguments: Dict[str, Any]) -> ToolResult:
        """Execute coverage report."""
        format_type = arguments.get("format", "term")

        try:
            project_path = self.agent.project.local_path
            if not project_path:
                return ToolResult(
                    success=False,
                    error="Project path not set"
                )

            # Build coverage command
            cmd = ["pytest", "--cov", f"--cov-report={format_type}"]

            # Run coverage
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300
            )

            output = result.stdout + result.stderr

            # Parse coverage percentage
            coverage_pct = self._parse_coverage(output)

            return ToolResult(
                success=True,
                result={
                    "format": format_type,
                    "coverage_percentage": coverage_pct,
                    "output": output
                }
            )

        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                error="Coverage generation timed out"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Failed to generate coverage: {str(e)}"
            )

    def _parse_coverage(self, output: str) -> float:
        """Parse coverage percentage from output."""
        for line in output.split('\n'):
            if 'TOTAL' in line and '%' in line:
                try:
                    parts = line.split()
                    for part in parts:
                        if '%' in part:
                            return float(part.replace('%', ''))
                except:
                    pass
        return 0.0


class CreateTestTool(BaseTool):
    """Create a new test file."""

    name = "create_test"
    description = "Create a new test file with boilerplate code"

    parameters_schema = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path for the new test file (e.g., 'tests/test_models.py')"
            },
            "test_code": {
                "type": "string",
                "description": "Test code to write to the file"
            },
            "framework": {
                "type": "string",
                "enum": ["pytest", "unittest"],
                "description": "Testing framework to use",
                "default": "pytest"
            }
        },
        "required": ["file_path", "test_code"]
    }

    async def execute(self, arguments: Dict[str, Any]) -> ToolResult:
        """Execute test file creation."""
        file_path = arguments.get("file_path", "")
        test_code = arguments.get("test_code", "")
        framework = arguments.get("framework", "pytest")

        try:
            project_path = self.agent.project.local_path
            if not project_path:
                return ToolResult(
                    success=False,
                    error="Project path not set"
                )

            full_path = Path(project_path) / file_path

            # Create parent directories
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Check if file exists
            if full_path.exists():
                return ToolResult(
                    success=False,
                    error=f"Test file already exists: {file_path}"
                )

            # Add framework-specific imports if needed
            if framework == "pytest" and "import pytest" not in test_code:
                test_code = "import pytest\n\n" + test_code
            elif framework == "unittest" and "import unittest" not in test_code:
                test_code = "import unittest\n\n" + test_code

            # Write test file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(test_code)

            return ToolResult(
                success=True,
                result={
                    "file_path": file_path,
                    "framework": framework,
                    "line_count": len(test_code.splitlines())
                }
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Failed to create test file: {str(e)}"
            )
