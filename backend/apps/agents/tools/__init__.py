"""
Agent Tools

Collection of tools available to agents for executing tasks.
"""

from typing import Dict, Optional
from .base import BaseTool, ToolResult

# File tools
from .file_tools import (
    ReadFileTool,
    WriteFileTool,
    ModifyFileTool,
    DeleteFileTool
)

# Task tools
from .task_tools import (
    CreateTaskTool,
    UpdateTaskStatusTool,
    AssignTaskTool
)

# Communication tools
from .communication_tools import (
    SendMessageTool,
    AskUserTool,
    HireAgentTool
)

# Code analysis tools
from .code_tools import (
    SearchCodebaseTool,
    AnalyzeCodeTool,
    GetDependenciesTool
)

# Test tools
from .test_tools import (
    RunTestsTool,
    RunCoverageTool,
    CreateTestTool
)

# Linting and formatting tools
from .lint_tools import (
    FormatCodeTool,
    RunLinterTool,
    TypeCheckTool,
    SecurityCheckTool
)


class ToolRegistry:
    """
    Registry of all available tools.

    Provides lookup by name and tool definitions for LLMs.
    """

    def __init__(self):
        """Initialize registry with all tools."""
        self._tools: Dict[str, BaseTool] = {}

        # Register all tools
        self._register_tool(ReadFileTool())
        self._register_tool(WriteFileTool())
        self._register_tool(ModifyFileTool())
        self._register_tool(DeleteFileTool())

        self._register_tool(CreateTaskTool())
        self._register_tool(UpdateTaskStatusTool())
        self._register_tool(AssignTaskTool())

        self._register_tool(SendMessageTool())
        self._register_tool(AskUserTool())
        self._register_tool(HireAgentTool())

        # Code analysis tools
        self._register_tool(SearchCodebaseTool())
        self._register_tool(AnalyzeCodeTool())
        self._register_tool(GetDependenciesTool())

        # Test tools
        self._register_tool(RunTestsTool())
        self._register_tool(RunCoverageTool())
        self._register_tool(CreateTestTool())

        # Linting tools
        self._register_tool(FormatCodeTool())
        self._register_tool(RunLinterTool())
        self._register_tool(TypeCheckTool())
        self._register_tool(SecurityCheckTool())

    def _register_tool(self, tool: BaseTool):
        """Register a tool."""
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """
        Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None
        """
        return self._tools.get(name)

    def get_tool_definitions(self, tool_names: list[str] = None) -> list[Dict]:
        """
        Get tool definitions for LLM.

        Args:
            tool_names: List of tool names to include (None = all)

        Returns:
            List of tool definitions
        """
        if tool_names is None:
            # Return all tools
            return [tool.get_definition() for tool in self._tools.values()]

        # Return specific tools
        definitions = []
        for name in tool_names:
            tool = self._tools.get(name)
            if tool:
                definitions.append(tool.get_definition())

        return definitions

    def list_tools(self) -> list[str]:
        """Get list of all tool names."""
        return list(self._tools.keys())

    def has_tool(self, name: str) -> bool:
        """Check if tool exists."""
        return name in self._tools


# Create global registry instance
tool_registry = ToolRegistry()


# Convenience functions
def get_tool(name: str) -> Optional[BaseTool]:
    """Get a tool by name from global registry."""
    return tool_registry.get_tool(name)


def get_tool_definitions(tool_names: list[str] = None) -> list[Dict]:
    """Get tool definitions for LLM."""
    return tool_registry.get_tool_definitions(tool_names)


__all__ = [
    # Base classes
    'BaseTool',
    'ToolResult',

    # File tools
    'ReadFileTool',
    'WriteFileTool',
    'ModifyFileTool',
    'DeleteFileTool',

    # Task tools
    'CreateTaskTool',
    'UpdateTaskStatusTool',
    'AssignTaskTool',

    # Communication tools
    'SendMessageTool',
    'AskUserTool',
    'HireAgentTool',

    # Code analysis tools
    'SearchCodebaseTool',
    'AnalyzeCodeTool',
    'GetDependenciesTool',

    # Test tools
    'RunTestsTool',
    'RunCoverageTool',
    'CreateTestTool',

    # Linting tools
    'FormatCodeTool',
    'RunLinterTool',
    'TypeCheckTool',
    'SecurityCheckTool',

    # Registry
    'ToolRegistry',
    'tool_registry',
    'get_tool',
    'get_tool_definitions',
]
