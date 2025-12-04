"""Project WebSocket consumer for project mode."""

import json
import time
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import Project, ProjectFile
from apps.chat.models import Conversation, Message
from services.crew_service import CrewService
from services.usage_service import UsageService

User = get_user_model()
logger = logging.getLogger(__name__)


class ProjectConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for project mode with CrewAI multi-agent system."""

    async def connect(self):
        """Handle WebSocket connection."""
        self.user = self.scope.get('user')

        if not self.user or not self.user.is_authenticated:
            await self.close(code=4001)
            return

        # Get project ID from URL
        self.project_id = self.scope['url_route']['kwargs']['project_id']

        # Verify user owns the project
        self.project = await self.get_project()
        if not self.project:
            await self.close(code=4004)
            return

        await self.accept()

        # Send initial project state
        await self.send_project_state()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        pass

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'crew_message':
                await self.handle_crew_message(data)
            elif message_type == 'get_file':
                await self.handle_get_file(data)
            elif message_type == 'ping':
                await self.send(text_data=json.dumps({'type': 'pong'}))
            else:
                await self.send_error(f'Unknown message type: {message_type}')

        except json.JSONDecodeError:
            await self.send_error('Invalid JSON')
        except Exception as e:
            logger.exception(f"Error handling message: {e}")
            await self.send_error(str(e))

    async def handle_crew_message(self, data):
        """Handle user message for CrewAI multi-agent pipeline."""
        message_content = data.get('message')
        continue_from_last = data.get('continue', False)

        logger.info(f"[CREW] Received message for project {self.project_id}: {message_content[:100]}...")

        if not message_content:
            await self.send_error('Message content is required')
            return

        # Check usage limits
        can_request, used, limit = await self.check_project_limit()
        if not can_request:
            logger.warning(f"[CREW] Usage limit exceeded for user {self.user.id}")
            await self.send_limit_error('project', used, limit)
            return

        # Get or create project conversation
        conversation = await self.get_or_create_conversation()
        logger.info(f"[CREW] Using conversation {conversation.id}")

        # Save user message
        await self.save_message(conversation, 'user', message_content)
        logger.info(f"[CREW] User message saved")

        # Send acknowledgment
        await self.send(text_data=json.dumps({
            'type': 'message_received',
            'message': message_content
        }))

        # Execute CrewAI pipeline
        crew_service = CrewService()
        start_time = time.time()

        try:
            logger.info(f"[CREW] Starting CrewAI pipeline...")

            async for event in crew_service.execute_development_crew(
                project=self.project,
                project_description=message_content,
                continue_from_last=continue_from_last,
            ):
                logger.debug(f"[CREW] Event: {event.get('type')}")
                await self.send(text_data=json.dumps(event))

            # Record usage
            duration_ms = int((time.time() - start_time) * 1000)
            await self.record_project_usage(
                project_id=str(self.project.id),
                duration_ms=duration_ms
            )
            logger.info(f"[CREW] Usage recorded ({duration_ms}ms)")

            # Save completion message
            completion_msg = (
                "✓ CrewAI Development Team completed!\n\n"
                "All agents have finished their tasks. Your project is ready!"
            )
            await self.save_message(conversation, 'agent', completion_msg)

            # Send done event
            await self.send(text_data=json.dumps({'type': 'done'}))

        except Exception as e:
            logger.exception(f"[CREW] Error during CrewAI execution: {e}")
            await self.send_error(str(e))

    async def handle_get_file(self, data):
        """Handle request to get file content."""
        path = data.get('path')

        if not path:
            await self.send_error('File path is required')
            return

        file = await self.get_file(path)

        if file:
            await self.send(text_data=json.dumps({
                'type': 'file_content',
                'path': file.path,
                'content': file.content,
                'language': file.language
            }))
        else:
            await self.send_error(f'File not found: {path}')

    async def send_project_state(self):
        """Send current project state to client."""
        files = await self.get_project_files()
        conversation = await self.get_or_create_conversation()
        messages = await self.get_conversation_messages(conversation)

        tree = await database_sync_to_async(self.project.get_file_tree)()

        await self.send(text_data=json.dumps({
            'type': 'project_state',
            'project': {
                'id': str(self.project.id),
                'name': self.project.name,
                'description': self.project.description,
                'status': self.project.status,
                'file_tree': tree,
            },
            'files': [
                {'path': f.path, 'language': f.language}
                for f in files
            ],
            'messages': [
                {
                    'id': str(m.id),
                    'role': m.role,
                    'content': m.content,
                    'agent': m.agent_name,
                    'created_at': m.created_at.isoformat()
                }
                for m in messages
            ]
        }))

    async def send_error(self, error_message):
        """Send error message to client."""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'error': error_message
        }))

    # Database operations

    @database_sync_to_async
    def get_project(self):
        try:
            return Project.objects.get(id=self.project_id, user=self.user)
        except Project.DoesNotExist:
            return None

    @database_sync_to_async
    def get_project_files(self):
        return list(self.project.files.all().order_by('path'))

    @database_sync_to_async
    def get_file(self, path):
        try:
            return self.project.files.get(path=path)
        except ProjectFile.DoesNotExist:
            return None

    @database_sync_to_async
    def get_or_create_conversation(self):
        conversation, _ = Conversation.objects.get_or_create(
            user=self.user,
            project=self.project,
            is_project_chat=True,
            defaults={'title': f'Chat - {self.project.name}'}
        )
        return conversation

    @database_sync_to_async
    def get_conversation_messages(self, conversation):
        return list(conversation.messages.order_by('created_at')[:100])

    @database_sync_to_async
    def save_message(self, conversation, role, content, agent_name=None):
        return Message.objects.create(
            conversation=conversation,
            role=role,
            content=content,
            agent_name=agent_name
        )

    # Usage tracking operations

    @database_sync_to_async
    def check_project_limit(self):
        """Check if user can make project request."""
        return UsageService.check_project_request_limit(self.user)

    @database_sync_to_async
    def record_project_usage(self, project_id, duration_ms=0):
        """Record project request usage."""
        return UsageService.record_project_request(
            user=self.user,
            project_id=project_id,
            duration_ms=duration_ms,
            model_used='crewai'
        )

    async def send_limit_error(self, limit_type, used, limit):
        """Send limit exceeded error with usage info."""
        usage_summary = await self.get_usage_summary()
        await self.send(text_data=json.dumps({
            'type': 'limit_exceeded',
            'limit_type': limit_type,
            'used': used,
            'limit': limit,
            'window_info': {
                'minutes_until_reset': usage_summary['window']['minutes_until_reset']
            },
            'message': f'You have reached your {limit_type} limit ({used}/{limit}). '
                      f'Resets in {usage_summary["window"]["minutes_until_reset"]} minutes. '
                      f'Upgrade to Pro for higher limits!'
        }))

    @database_sync_to_async
    def get_usage_summary(self):
        """Get current usage summary."""
        return UsageService.get_usage_summary(self.user)
