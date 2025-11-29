"""
Prompt Service

Handles prompt construction, formatting, and response parsing.
"""

import logging
from typing import Dict, Any, List, Optional
from apps.llm.clients.base import LLMResponse

logger = logging.getLogger(__name__)


class PromptService:
    """Service for constructing and formatting prompts."""

    @staticmethod
    def build_system_prompt(
        agent_type: str,
        persona: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Build a complete system prompt for an agent.

        Args:
            agent_type: Type of agent (orchestrator, architect, etc.)
            persona: Base persona/system prompt
            context: Additional context to include

        Returns:
            Complete system prompt
        """
        sections = [persona]

        if context:
            # Add project context
            if 'project' in context:
                project = context['project']
                sections.append(f"""
## Current Project
**Name**: {project.get('name', 'Unknown')}
**Status**: {project.get('status', 'Unknown')}
**Description**: {project.get('description', '')}
""")

            # Add task context
            if 'current_task' in context:
                sections.append(f"\n{context['current_task']}")

            # Add agent states
            if 'agent_states' in context:
                agent_list = "\n".join([
                    f"- {a['type']}: {a['status']}"
                    for a in context['agent_states']
                ])
                sections.append(f"""
## Other Active Agents
{agent_list}
""")

        return "\n\n".join(sections)

    @staticmethod
    def build_messages(
        conversation_history: List[Dict[str, str]],
        current_prompt: str
    ) -> List[Dict[str, str]]:
        """
        Build message history for LLM.

        Args:
            conversation_history: Previous conversation messages
            current_prompt: Current user prompt

        Returns:
            List of message dicts
        """
        messages = []

        # Add conversation history (last 20 messages)
        for msg in conversation_history[-20:]:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        # Add current prompt
        if current_prompt:
            messages.append({
                "role": "user",
                "content": current_prompt
            })

        return messages

    @staticmethod
    def format_task_prompt(task: Dict[str, Any]) -> str:
        """
        Format a task as a prompt for an agent.

        Args:
            task: Task data

        Returns:
            Formatted task prompt
        """
        prompt = f"""## Your Current Task

**{task.get('title', 'Untitled Task')}**

Type: {task.get('task_type', 'task')}
Priority: {task.get('priority', 'medium')}
Status: {task.get('status', 'todo')}

### Description
{task.get('description', 'No description provided')}
"""

        # Add requirements
        requirements = task.get('requirements', {})
        if requirements:
            prompt += "\n### Requirements\n"
            for key, value in requirements.items():
                if isinstance(value, list):
                    prompt += f"\n**{key}:**\n"
                    for item in value:
                        prompt += f"- {item}\n"
                else:
                    prompt += f"- **{key}:** {value}\n"

        # Add acceptance criteria
        criteria = task.get('acceptance_criteria', [])
        if criteria:
            prompt += "\n### Acceptance Criteria\n"
            for criterion in criteria:
                prompt += f"- [ ] {criterion}\n"

        # Add deliverables
        deliverables = task.get('deliverables', [])
        if deliverables:
            prompt += "\n### Expected Deliverables\n"
            for deliverable in deliverables:
                prompt += f"- {deliverable}\n"

        return prompt

    @staticmethod
    def extract_code_blocks(text: str) -> List[Dict[str, str]]:
        """
        Extract code blocks from markdown text.

        Args:
            text: Text containing code blocks

        Returns:
            List of dicts with 'language' and 'code'
        """
        import re

        pattern = r"```(\w+)?\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)

        code_blocks = []
        for language, code in matches:
            code_blocks.append({
                'language': language or 'text',
                'code': code.strip()
            })

        return code_blocks

    @staticmethod
    def parse_agent_response(response_text: str) -> LLMResponse:
        """
        Parse agent response text into structured format.

        This is a wrapper around the client's parse_response
        that adds additional DEVO-specific parsing.

        Args:
            response_text: Raw response text

        Returns:
            Structured LLMResponse
        """
        # This will be enhanced with DEVO-specific parsing
        # For now, it's a placeholder that returns basic structure

        return LLMResponse(
            content=response_text,
            thinking="",
            tool_calls=[],
            is_final=True
        )
