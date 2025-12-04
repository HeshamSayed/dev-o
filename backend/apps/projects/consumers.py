"""Project WebSocket consumer for project mode."""

import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import Project, ProjectFile
from apps.chat.models import Conversation, Message
from services.usage_service import UsageService

User = get_user_model()
logger = logging.getLogger(__name__)


class ProjectConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for project mode."""

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

            if message_type == 'get_file':
                await self.handle_get_file(data)
            elif message_type == 'ping':
                await self.send(text_data=json.dumps({'type': 'pong'}))
            else:
                await self.send_error(f'Unknown message type: {message_type}')

        except json.JSONDecodeError:
            await self.send_error('Invalid JSON')
        except Exception as e:
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
    def save_message(self, conversation, role, content):
        return Message.objects.create(
            conversation=conversation,
            role=role,
            content=content
        )
