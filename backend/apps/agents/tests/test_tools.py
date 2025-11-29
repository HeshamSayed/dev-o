"""
Unit tests for agent tools.
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

from apps.agents.tools.file_tools import (
    ReadFileTool,
    WriteFileTool,
    ModifyFileTool,
    DeleteFileTool
)
from apps.agents.tools.task_tools import (
    CreateTaskTool,
    UpdateTaskStatusTool,
    AssignTaskTool
)
from apps.agents.tools.code_tools import (
    SearchCodebaseTool,
    AnalyzeCodeTool
)
from apps.agents.tools.test_tools import (
    RunTestsTool,
    CreateTestTool
)
from apps.agents.tools.lint_tools import (
    FormatCodeTool,
    RunLinterTool
)
from apps.projects.tests.factories import ProjectFactory
from apps.agents.tests.factories import AgentInstanceFactory


@pytest.mark.django_db
class TestFileTools:
    """Tests for file tools."""

    @pytest.fixture
    def temp_project_dir(self, tmp_path):
        """Create temporary project directory."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        return project_dir

    @pytest.fixture
    def agent_with_project(self, temp_project_dir):
        """Create agent with project that has local path."""
        project = ProjectFactory(local_path=str(temp_project_dir))
        agent = AgentInstanceFactory(project=project)
        return agent

    @pytest.mark.asyncio
    async def test_read_file_tool(self, agent_with_project, temp_project_dir):
        """Test reading a file."""
        # Create test file
        test_file = temp_project_dir / "test.txt"
        test_file.write_text("Hello, World!")

        tool = ReadFileTool()
        tool.agent = agent_with_project

        result = await tool.execute({"file_path": "test.txt"})

        assert result.success is True
        assert result.result["content"] == "Hello, World!"
        assert result.result["line_count"] == 1

    @pytest.mark.asyncio
    async def test_write_file_tool(self, agent_with_project, temp_project_dir):
        """Test writing a file."""
        tool = WriteFileTool()
        tool.agent = agent_with_project

        result = await tool.execute({
            "file_path": "new_file.txt",
            "content": "New content"
        })

        assert result.success is True
        assert result.result["file_path"] == "new_file.txt"

        # Verify file was created
        new_file = temp_project_dir / "new_file.txt"
        assert new_file.exists()
        assert new_file.read_text() == "New content"

    @pytest.mark.asyncio
    async def test_modify_file_tool(self, agent_with_project, temp_project_dir):
        """Test modifying a file."""
        # Create test file
        test_file = temp_project_dir / "test.py"
        test_file.write_text("def hello():\n    print('Hello')")

        tool = ModifyFileTool()
        tool.agent = agent_with_project

        result = await tool.execute({
            "file_path": "test.py",
            "old_content": "print('Hello')",
            "new_content": "print('Hello, World!')"
        })

        assert result.success is True
        assert "Hello, World!" in test_file.read_text()

    @pytest.mark.asyncio
    async def test_delete_file_tool(self, agent_with_project, temp_project_dir):
        """Test deleting a file."""
        # Create test file
        test_file = temp_project_dir / "to_delete.txt"
        test_file.write_text("Delete me")

        tool = DeleteFileTool()
        tool.agent = agent_with_project

        result = await tool.execute({"file_path": "to_delete.txt"})

        assert result.success is True
        # File should be soft-deleted (moved to .deleted)
        deleted_file = temp_project_dir / ".deleted" / "to_delete.txt"
        assert deleted_file.exists()


@pytest.mark.django_db
class TestTaskTools:
    """Tests for task tools."""

    @pytest.fixture
    def agent_with_project(self):
        """Create agent with project."""
        project = ProjectFactory()
        agent = AgentInstanceFactory(project=project)
        return agent

    @pytest.mark.asyncio
    async def test_create_task_tool(self, agent_with_project):
        """Test creating a task."""
        tool = CreateTaskTool()
        tool.agent = agent_with_project

        result = await tool.execute({
            "title": "Test Task",
            "description": "Test description",
            "task_type": "task",
            "priority": 2
        })

        assert result.success is True
        assert result.result["title"] == "Test Task"
        assert result.result["status"] == "todo"

    @pytest.mark.asyncio
    async def test_update_task_status_tool(self, agent_with_project):
        """Test updating task status."""
        from apps.tasks.tests.factories import TaskFactory

        task = TaskFactory(project=agent_with_project.project, status="todo")

        tool = UpdateTaskStatusTool()
        tool.agent = agent_with_project

        result = await tool.execute({
            "task_id": str(task.id),
            "status": "in_progress"
        })

        assert result.success is True

        # Verify task was updated
        task.refresh_from_db()
        assert task.status == "in_progress"


@pytest.mark.django_db
class TestCodeAnalysisTools:
    """Tests for code analysis tools."""

    @pytest.fixture
    def temp_project_dir(self, tmp_path):
        """Create temporary project directory with Python files."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()

        # Create test Python file
        test_file = project_dir / "test.py"
        test_file.write_text("""
import os
from pathlib import Path

class TestClass:
    def __init__(self):
        self.value = 0

    def test_method(self):
        return self.value

def test_function(arg1, arg2):
    return arg1 + arg2
""")
        return project_dir

    @pytest.fixture
    def agent_with_project(self, temp_project_dir):
        """Create agent with project."""
        project = ProjectFactory(local_path=str(temp_project_dir))
        agent = AgentInstanceFactory(project=project)
        return agent

    @pytest.mark.asyncio
    async def test_search_codebase_text(self, agent_with_project, temp_project_dir):
        """Test text search in codebase."""
        tool = SearchCodebaseTool()
        tool.agent = agent_with_project

        result = await tool.execute({
            "query": "TestClass",
            "search_type": "text",
            "file_pattern": "*.py"
        })

        assert result.success is True
        assert result.result["results_count"] > 0
        assert any("TestClass" in r["content"] for r in result.result["results"])

    @pytest.mark.asyncio
    async def test_analyze_code_tool(self, agent_with_project):
        """Test code analysis."""
        tool = AnalyzeCodeTool()
        tool.agent = agent_with_project

        result = await tool.execute({"file_path": "test.py"})

        assert result.success is True
        assert result.result["class_count"] == 1
        assert result.result["function_count"] >= 1
        assert result.result["import_count"] == 2


@pytest.mark.django_db
class TestTestTools:
    """Tests for testing tools."""

    @pytest.fixture
    def agent_with_project(self, tmp_path):
        """Create agent with project."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()

        project = ProjectFactory(local_path=str(project_dir))
        agent = AgentInstanceFactory(project=project)
        return agent

    @pytest.mark.asyncio
    async def test_create_test_tool(self, agent_with_project):
        """Test creating a test file."""
        tool = CreateTestTool()
        tool.agent = agent_with_project

        result = await tool.execute({
            "file_path": "tests/test_example.py",
            "test_code": "def test_example():\n    assert True",
            "framework": "pytest"
        })

        assert result.success is True

        # Verify file was created
        project_path = Path(agent_with_project.project.local_path)
        test_file = project_path / "tests" / "test_example.py"
        assert test_file.exists()
        assert "import pytest" in test_file.read_text()

    @pytest.mark.asyncio
    @patch('subprocess.run')
    async def test_run_tests_tool(self, mock_run, agent_with_project):
        """Test running tests."""
        # Mock pytest output
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="5 passed in 1.23s",
            stderr=""
        )

        tool = RunTestsTool()
        tool.agent = agent_with_project

        result = await tool.execute({
            "test_path": "",
            "verbose": True
        })

        assert result.success is True
        assert result.result["passed"] is True
        assert mock_run.called


@pytest.mark.django_db
class TestLintingTools:
    """Tests for linting tools."""

    @pytest.fixture
    def agent_with_project(self, tmp_path):
        """Create agent with project."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()

        # Create test Python file
        test_file = project_dir / "test.py"
        test_file.write_text("x=1\ny  =  2\n")  # Badly formatted

        project = ProjectFactory(local_path=str(project_dir))
        agent = AgentInstanceFactory(project=project)
        return agent

    @pytest.mark.asyncio
    @patch('subprocess.run')
    async def test_format_code_tool(self, mock_run, agent_with_project):
        """Test code formatting."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="1 file reformatted",
            stderr=""
        )

        tool = FormatCodeTool()
        tool.agent = agent_with_project

        result = await tool.execute({
            "file_path": "test.py",
            "check_only": False
        })

        assert result.success is True
        assert mock_run.called

    @pytest.mark.asyncio
    @patch('subprocess.run')
    async def test_run_linter_tool(self, mock_run, agent_with_project):
        """Test running linter."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="test.py:1:1: E501 line too long",
            stderr=""
        )

        tool = RunLinterTool()
        tool.agent = agent_with_project

        result = await tool.execute({
            "file_path": "test.py",
            "fix": False
        })

        assert result.success is True
        assert result.result["has_issues"] is True
        assert mock_run.called
