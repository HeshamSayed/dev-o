"""
Base Tool Interface

All agent tools inherit from BaseTool and implement execute() method.
Tools are the primary way agents interact with the system.
"""

import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ToolResult:
    """
    Standard result format for all tools.

    Attributes:
        success: Whether the tool executed successfully
        message: Human-readable result message
        data: Additional result data (optional)
        is_reversible: Whether this action can be undone
        reverse_action: Data needed to reverse this action
        error_code: Error code if failed (optional)
    """
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    is_reversible: bool = False
    reverse_action: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "is_reversible": self.is_reversible,
            "reverse_action": self.reverse_action,
            "error_code": self.error_code
        }


class BaseTool(ABC):
    """
    Base class for all agent tools.

    Each tool must implement:
    - name: Unique tool identifier
    - description: What the tool does
    - parameters_schema: JSON schema for parameters
    - execute: Tool execution logic
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool name (e.g., 'read_file')."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what this tool does."""
        pass

    @property
    @abstractmethod
    def parameters_schema(self) -> Dict[str, Any]:
        """
        JSON schema describing the tool's parameters.

        Example:
        {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to file"},
                "content": {"type": "string", "description": "File content"}
            },
            "required": ["file_path", "content"]
        }
        """
        pass

    @abstractmethod
    async def execute(
        self,
        arguments: Dict[str, Any],
        context: Dict[str, Any]
    ) -> ToolResult:
        """
        Execute the tool with given arguments.

        Args:
            arguments: Tool parameters from LLM
            context: Execution context (agent, task, project)

        Returns:
            ToolResult with execution outcome
        """
        pass

    def validate_arguments(self, arguments: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate arguments against schema.

        Args:
            arguments: Arguments to validate

        Returns:
            (is_valid, error_message)
        """
        schema = self.parameters_schema
        required = schema.get("required", [])

        # Check required fields
        for field in required:
            if field not in arguments:
                return False, f"Missing required parameter: {field}"

        # Check types (basic validation)
        properties = schema.get("properties", {})
        for key, value in arguments.items():
            if key in properties:
                expected_type = properties[key].get("type")
                actual_type = type(value).__name__

                # Map Python types to JSON schema types
                type_map = {
                    "str": "string",
                    "int": "integer",
                    "float": "number",
                    "bool": "boolean",
                    "list": "array",
                    "dict": "object"
                }

                if type_map.get(actual_type) != expected_type:
                    return False, f"Parameter '{key}' should be {expected_type}, got {actual_type}"

        return True, None

    def get_definition(self) -> Dict[str, Any]:
        """
        Get tool definition for LLM.

        Returns tool in format expected by LLM for tool calling.
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters_schema
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"
