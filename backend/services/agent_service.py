"""Service for orchestrating AI agents in project mode."""

import re
from typing import AsyncGenerator, Dict, Any, List, Optional
from django.db import transaction
from channels.db import database_sync_to_async

from apps.projects.models import Project, ProjectFile
from apps.agents.models import Agent
from .ai_service import AIService
import logging

logger = logging.getLogger(__name__)


class AgentService:
    """Service for orchestrating AI agents in project mode."""

    def __init__(self):
        self.ai_service = AIService()

    @database_sync_to_async
    def get_project_context(self, project: Project) -> Dict[str, Any]:
        """Get full project context for agents."""
        files = list(project.files.all())

        return {
            'project_id': str(project.id),
            'project_name': project.name,
            'project_type': project.project_type,
            'file_tree': project.get_file_tree(),
            'files': [
                {
                    'path': f.path,
                    'content': f.content,
                    'language': f.language
                }
                for f in files
            ],
            'file_count': len(files),
        }

    @database_sync_to_async
    def select_agent(
        self,
        project: Project,
        user_message: str
    ) -> Optional[Agent]:
        """Select the appropriate agent based on task."""
        # Get assigned agents
        assignments = project.agent_assignments.filter(is_active=True).select_related('agent')
        agents = [a.agent for a in assignments]

        if not agents:
            return None

        # Simple keyword-based selection
        message_lower = user_message.lower()

        for agent in agents:
            if agent.type == 'backend' and any(kw in message_lower for kw in
                ['backend', 'django', 'api', 'model', 'database', 'python', 'server']):
                return agent
            elif agent.type == 'frontend' and any(kw in message_lower for kw in
                ['frontend', 'react', 'ui', 'component', 'page', 'css', 'style']):
                return agent
            elif agent.type == 'devops' and any(kw in message_lower for kw in
                ['docker', 'deploy', 'nginx', 'ci', 'cd', 'kubernetes']):
                return agent

        # Default to first agent or fullstack if available
        fullstack = next((a for a in agents if a.type == 'fullstack'), None)
        return fullstack or agents[0]

    def parse_ai_response(self, content: str) -> Dict[str, Any]:
        """Parse AI response for file operations and thinking."""
        result = {
            'thinking': None,
            'files': [],
            'chat_content': content
        }

        # Extract thinking blocks
        thinking_pattern = r'<thinking>(.*?)</thinking>'
        thinking_matches = re.findall(thinking_pattern, content, re.DOTALL)
        if thinking_matches:
            result['thinking'] = '\n'.join(thinking_matches)

        # Extract file blocks
        file_pattern = r'<file path="([^"]+)">(.*?)</file>'
        file_matches = re.findall(file_pattern, content, re.DOTALL)
        for path, file_content in file_matches:
            result['files'].append({
                'path': path.strip(),
                'content': file_content.strip()
            })

        # Remove file and thinking blocks from chat content
        clean_content = re.sub(r'<file path="[^"]+">.*?</file>', '', content, flags=re.DOTALL)
        clean_content = re.sub(r'<thinking>.*?</thinking>', '', clean_content, flags=re.DOTALL)
        result['chat_content'] = clean_content.strip()

        return result

    async def execute_agent(
        self,
        project: Project,
        agent: Agent,
        user_message: str,
        conversation,
        show_thinking: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute agent task and stream results."""

        logger.info(f"[AGENT] Starting execution for project {project.id} with agent {agent.name}")
        logger.info(f"[AGENT] User message: {user_message[:100]}...")

        # Get project context
        context = await self.get_project_context(project)
        logger.info(f"[AGENT] Project context: {context['file_count']} files")

        # Build agent system prompt
        system_prompt = self.ai_service.build_agent_system_prompt(
            agent_type=agent.type,
            agent_prompt=agent.system_prompt,
            project_context=context
        )

        # Get conversation history
        history = await self._get_conversation_history(conversation)

        # Prepare messages
        messages = self.ai_service.prepare_messages(
            system_prompt=system_prompt,
            history=history,
            user_message=user_message
        )

        # Stream AI response
        full_response = []
        buffer = ''  # Buffer for converting markdown to file tags in real-time

        logger.info("[AGENT] Starting AI stream...")
        async for chunk in self.ai_service.stream_chat(messages):
            if chunk['type'] == 'error':
                logger.error(f"[AGENT] AI error: {chunk['error']}")
                yield {'type': 'error', 'error': chunk['error']}
                break

            if chunk['type'] == 'done':
                # Process any remaining buffer
                if buffer:
                    converted = self._convert_markdown_to_file_tags(buffer)
                    for token in converted:
                        yield {'type': 'token', 'content': token}

                # Parse complete response
                full_text = ''.join(full_response)
                logger.info(f"[AGENT] AI response complete. Length: {len(full_text)} chars")
                parsed = self.parse_ai_response(full_text)
                logger.info(f"[AGENT] Parsed {len(parsed['files'])} files from response")

                # Save files
                for file_info in parsed['files']:
                    logger.info(f"[AGENT] Saving file: {file_info['path']}")
                    await self.save_file(
                        project=project,
                        path=file_info['path'],
                        content=file_info['content'],
                        agent=agent
                    )
                    logger.info(f"[AGENT] File saved successfully: {file_info['path']}")
                    yield {
                        'type': 'file_created',
                        'path': file_info['path']
                    }

                # Send file tree update
                context = await self.get_project_context(project)
                yield {
                    'type': 'file_tree_update',
                    'tree': context['file_tree']
                }

                # Send thinking if enabled
                if show_thinking and parsed['thinking']:
                    yield {
                        'type': 'thinking',
                        'content': parsed['thinking']
                    }

                yield {'type': 'done'}
                break

            if chunk['type'] == 'content':
                content = chunk['content']
                full_response.append(content)

                # Add to buffer
                buffer += content

                # Convert markdown code blocks to file tags in real-time
                converted, buffer = self._stream_convert_markdown(buffer)
                for token in converted:
                    yield {'type': 'token', 'content': token}

    def _stream_convert_markdown(self, buffer: str) -> tuple[list[str], str]:
        """
        Convert markdown code blocks to file tags in REAL-TIME streaming fashion.
        Returns: (list of tokens to send, remaining buffer)
        """
        import re

        tokens_to_send = []

        # Check if we're currently inside a code block (stored in class state if needed)
        # For simplicity, detect opening and closing separately

        # Pattern 1: Opening - "Creating `filename`:\n```language\n"
        opening_pattern = r'Creating\s+[`\'"]([\w./]+\.\w+)[`\'"][^\n]*\n```\w*\s*\n'
        opening_match = re.search(opening_pattern, buffer)

        if opening_match:
            # Send everything before the match as-is
            before = buffer[:opening_match.start()]
            if before:
                tokens_to_send.append(before)

            # Extract filename from the match
            filename = opening_match.group(1)

            # Send the "Creating..." line
            creating_line = buffer[opening_match.start():buffer.find('\n', opening_match.start()) + 1]
            tokens_to_send.append(creating_line)

            # Send opening file tag
            tokens_to_send.append(f'<file path="{filename}">\n')

            # Everything after the ``` opening goes into buffer for code streaming
            code_start = opening_match.end()
            remaining = buffer[code_start:]

            # Check if there's a closing ``` in the remaining part
            closing_match = re.search(r'```', remaining)
            if closing_match:
                # Complete block! Send code and close tag
                code = remaining[:closing_match.start()]
                tokens_to_send.append(code)
                tokens_to_send.append('</file>\n')

                # Return everything after closing ```
                return tokens_to_send, remaining[closing_match.end():]
            else:
                # Incomplete block - send all code so far, keep buffer for more
                if len(remaining) > 100:  # Send in chunks
                    # Send most of it, keep last 100 chars in case closing tag is split
                    to_send = remaining[:-100]
                    tokens_to_send.append(to_send)
                    return tokens_to_send, remaining[-100:]
                else:
                    # Too small, keep in buffer
                    return tokens_to_send, remaining
        else:
            # No opening tag found
            # Check if we should send part of buffer (avoid infinite buffering)
            if len(buffer) > 500 and 'Creating' not in buffer[-200:]:
                # Send most of buffer, keep last 200 chars
                tokens_to_send.append(buffer[:-200])
                return tokens_to_send, buffer[-200:]

        return tokens_to_send, buffer

    def _convert_markdown_to_file_tags(self, text: str) -> list[str]:
        """Convert any remaining markdown in buffer to file tags."""
        tokens, _ = self._stream_convert_markdown(text)
        return tokens

    @database_sync_to_async
    def _get_conversation_history(self, conversation):
        """Get conversation history."""
        return list(conversation.messages.order_by('created_at')[:30])

    @database_sync_to_async
    def save_file(
        self,
        project: Project,
        path: str,
        content: str,
        agent: Agent
    ) -> ProjectFile:
        """Save or update a project file."""
        file, created = ProjectFile.objects.update_or_create(
            project=project,
            path=path,
            defaults={
                'content': content,
                'created_by_agent': agent,
            }
        )

        if not created:
            file.version += 1
            file.save()

        return file
