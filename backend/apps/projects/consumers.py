"""
WebSocket consumer for multi-agent conversations.

Handles real-time streaming of multi-agent conversations where agents
discuss requirements, architecture, and implementation in front of the user.
"""
import json
import asyncio
import logging
from typing import Dict, Any
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from apps.projects.models import Project
from apps.agents.engine.conversation_orchestrator import ConversationOrchestrator

logger = logging.getLogger(__name__)


class ProjectExecutionConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for multi-agent conversations.

    Receives user messages and orchestrates multi-agent conversations
    where agents discuss requirements, architecture, and implementation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_id = None
        self.project = None
        self.user = None
        self.conversation_orchestrator: Optional[ConversationOrchestrator] = None
        self.conversation_task = None

    async def connect(self):
        """Handle WebSocket connection."""
        # Get project ID from URL
        self.project_id = self.scope['url_route']['kwargs']['project_id']

        # Get user from scope (set by AuthMiddlewareStack)
        self.user = self.scope.get('user')

        # Authenticate
        import sys
        sys.stderr.write(f"[CONSUMER DEBUG] User: {self.user}, Authenticated: {self.user.is_authenticated if self.user else False}\n")
        sys.stderr.flush()
        if not self.user or not self.user.is_authenticated:
            sys.stderr.write(f"[CONSUMER DEBUG] Rejecting: User not authenticated (code 4001)\n")
            sys.stderr.flush()
            await self.close(code=4001)
            return

        # Load project
        try:
            self.project = await self.get_project(self.project_id)
            sys.stderr.write(f"[CONSUMER DEBUG] Project loaded: {self.project.name} (ID: {self.project_id})\n")
            sys.stderr.flush()
        except ObjectDoesNotExist:
            sys.stderr.write(f"[CONSUMER DEBUG] Rejecting: Project not found (code 4004)\n")
            sys.stderr.flush()
            await self.close(code=4004)
            return

        # Check permissions
        sys.stderr.write(f"[CONSUMER DEBUG] Project owner: {self.project.owner}, Current user: {self.user}\n")
        sys.stderr.flush()
        if self.project.owner != self.user:
            sys.stderr.write(f"[CONSUMER DEBUG] Rejecting: User doesn't own project (code 4003)\n")
            sys.stderr.flush()
            await self.close(code=4003)
            return

        # Accept connection
        await self.accept()

        # Initialize conversation orchestrator
        self.conversation_orchestrator = ConversationOrchestrator(self.project)
        await self.conversation_orchestrator.initialize_agents()

        # Send connection success
        await self.send_event({
            'type': 'connected',
            'project_id': str(self.project_id),
            'project_name': self.project.name,
            'message': 'Connected! Start chatting with Alex and the team.',
        })

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Cancel any running conversation
        if self.conversation_task and not self.conversation_task.done():
            self.conversation_task.cancel()
            try:
                await self.conversation_task
            except asyncio.CancelledError:
                pass

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'user_message':
                # User sent a message to execute
                await self.handle_user_message(data.get('content', ''))

            elif message_type == 'user_input':
                # User provided input in response to agent question
                await self.handle_user_input(data.get('content', ''))

            elif message_type == 'cancel':
                # Cancel current execution
                await self.handle_cancel()

            else:
                await self.send_error(f"Unknown message type: {message_type}")

        except json.JSONDecodeError:
            await self.send_error("Invalid JSON")
        except Exception as e:
            await self.send_error(f"Error processing message: {str(e)}")

    async def handle_user_message(self, message: str):
        """Handle user message and start multi-agent conversation."""
        if not message.strip():
            await self.send_error("Empty message")
            return

        if not self.conversation_orchestrator:
            await self.send_error("Conversation not initialized")
            return

        # Start conversation in background
        self.conversation_task = asyncio.create_task(
            self.process_conversation(message)
        )

    async def process_conversation(self, message: str):
        """Process user message through conversation orchestrator."""
        try:
            # Stream conversation events
            async for event in self.conversation_orchestrator.process_user_message(message):
                await self.send_event(event)

        except asyncio.CancelledError:
            await self.send_event({
                'type': 'cancelled',
                'message': 'Conversation cancelled',
            })
        except Exception as e:
            logger.exception(f"Error in conversation: {e}")
            await self.send_event({
                'type': 'error',
                'error': str(e),
                'recoverable': False,
            })

    async def handle_user_input(self, response: str):
        """Handle user input response."""
        # In a full implementation, this would send the input to the waiting agent
        # For now, just acknowledge
        await self.send_event({
            'type': 'user_input_received',
            'content': response,
        })

    async def handle_cancel(self):
        """Handle conversation cancellation."""
        if self.conversation_task and not self.conversation_task.done():
            self.conversation_task.cancel()
            await self.send_event({
                'type': 'cancelled',
                'message': 'Conversation cancelled by user',
            })
        else:
            await self.send_error("No active conversation to cancel")

    async def send_event(self, event: Dict[str, Any]):
        """Send event to WebSocket with immediate flush."""
        await self.send(text_data=json.dumps(event))
        # Force immediate send by awaiting (no buffering)
        await asyncio.sleep(0)  # Yield control to ensure send completes

    async def send_error(self, error: str):
        """Send error event."""
        await self.send_event({
            'type': 'error',
            'error': error,
            'recoverable': True,
        })

    # Database operations (sync_to_async wrapped)

    @database_sync_to_async
    def get_project(self, project_id):
        """Get project from database."""
        return Project.objects.select_related('owner').get(id=project_id)
