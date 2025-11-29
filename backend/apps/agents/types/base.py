"""
Base Agent Type Definition

This module defines the base structure for all agent types.
Each agent type has:
- Persona (system prompt)
- Available tools
- Hire capabilities
- Execution behavior
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class AgentPersona:
    """Defines an agent's personality and capabilities"""

    name: str
    role: str
    hierarchy_level: int

    # Core prompt
    system_prompt: str

    # Capabilities
    available_tools: List[str] = field(default_factory=list)
    can_hire: List[str] = field(default_factory=list)

    # Behavior modifiers
    thinking_style: str = "analytical"  # analytical, creative, practical
    verbosity: str = "normal"  # minimal, normal, detailed

    # Constraints
    max_iterations: int = 50
    max_files_per_task: int = 10
    requires_review_for: List[str] = field(default_factory=list)


@dataclass
class ToolCall:
    """Represents a tool call from an agent"""

    tool_name: str
    arguments: Dict[str, Any]
    reasoning: str = ""


class BaseAgentType(ABC):
    """
    Abstract base class for all agent types.

    Each agent type must implement:
    - persona property: Returns AgentPersona
    - get_system_prompt method: Builds context-aware system prompt
    """

    @property
    @abstractmethod
    def persona(self) -> AgentPersona:
        """
        Get agent's persona definition.

        Returns:
            AgentPersona with all agent characteristics
        """
        pass

    def get_system_prompt(self, context: Dict[str, Any]) -> str:
        """
        Build a complete system prompt with context.

        Args:
            context: Context dictionary with project info, tasks, etc.

        Returns:
            Complete system prompt for this agent
        """
        base_prompt = self.persona.system_prompt

        # Add context-specific information
        context_sections = []

        if context.get('project'):
            context_sections.append(self._format_project_context(context['project']))

        if context.get('current_task'):
            context_sections.append(f"\n{context['current_task']}")

        if context.get('agent_states'):
            context_sections.append(self._format_agent_states(context['agent_states']))

        if context.get('recent_changes'):
            context_sections.append(self._format_recent_changes(context['recent_changes']))

        if context_sections:
            return base_prompt + "\n\n" + "\n\n".join(context_sections)

        return base_prompt

    def _format_project_context(self, project: Dict[str, Any]) -> str:
        """Format project context."""
        return f"""## Current Project
**Name**: {project.get('name', 'Unknown')}
**Status**: {project.get('status', 'Unknown')}
**Description**: {project.get('description', '')}
"""

    def _format_agent_states(self, agents: List[Dict[str, Any]]) -> str:
        """Format other agents' states."""
        if not agents:
            return ""

        agent_list = "\n".join([
            f"- **{a['type']}**: {a['status']}" +
            (f" - {a.get('current_task', '')}" if a.get('current_task') else "")
            for a in agents
        ])

        return f"""## Other Active Agents
{agent_list}
"""

    def _format_recent_changes(self, changes: List[Dict[str, Any]]) -> str:
        """Format recent changes."""
        if not changes:
            return ""

        change_list = "\n".join([
            f"- [{c.get('timestamp', 'unknown')}] {c.get('agent', 'Unknown')}: {c.get('type', 'action')}"
            for c in changes[:10]  # Last 10 changes
        ])

        return f"""## Recent Changes
{change_list}
"""

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions for this agent.

        Returns:
            List of tool definitions in format expected by LLM
        """
        from apps.agents.tools import get_tool_definitions

        # Get tool definitions for this agent's available tools
        return get_tool_definitions(self.persona.available_tools)
