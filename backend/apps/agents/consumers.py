"""
WebSocket consumer for agent execution streaming.

Handles real-time streaming of individual agent execution events.
"""
import json
import asyncio
import logging
from typing import Dict, Any
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist

try:
    import orjson  # Fast JSON library for better performance
    USE_ORJSON = True
except ImportError:
    USE_ORJSON = False

from apps.agents.models import AgentInstance
from apps.agents.engine.runtime import AgentRuntime
from apps.tasks.models import Task

logger = logging.getLogger(__name__)


class AgentExecutionConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for agent-level execution.

    Receives task execution requests and streams agent execution events.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agent_id = None
        self.agent = None
        self.user = None
        self.execution_task = None

    async def connect(self):
        """Handle WebSocket connection."""
        # Get agent ID from URL
        self.agent_id = self.scope['url_route']['kwargs']['agent_id']

        # Get user from scope
        self.user = self.scope.get('user')

        # Authenticate
        if not self.user or not self.user.is_authenticated:
            await self.close(code=4001)
            return

        # Load agent
        try:
            self.agent = await self.get_agent(self.agent_id)
        except ObjectDoesNotExist:
            await self.close(code=4004)
            return

        # Check permissions (user must own the project)
        if self.agent.project.owner != self.user:
            await self.close(code=4003)
            return

        # Accept connection
        await self.accept()

        # Send connection success
        await self.send_event({
            'type': 'connected',
            'agent_id': str(self.agent_id),
            'agent_name': self.agent.agent_type.name,
            'agent_role': self.agent.agent_type.role,
        })

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Cancel any running execution
        if self.execution_task and not self.execution_task.done():
            self.execution_task.cancel()
            try:
                await self.execution_task
            except asyncio.CancelledError:
                pass

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'execute_task':
                # Execute specific task
                task_id = data.get('task_id')
                if task_id:
                    await self.handle_execute_task(task_id)
                else:
                    await self.send_error("Missing task_id")

            elif message_type == 'user_input':
                # User provided input
                await self.handle_user_input(data.get('content', ''))

            elif message_type == 'cancel':
                # Cancel execution
                await self.handle_cancel()

            else:
                await self.send_error(f"Unknown message type: {message_type}")

        except json.JSONDecodeError:
            await self.send_error("Invalid JSON")
        except Exception as e:
            await self.send_error(f"Error processing message: {str(e)}")

    async def handle_execute_task(self, task_id: str):
        """Handle task execution request."""
        # Load task
        try:
            task = await self.get_task(task_id)
        except ObjectDoesNotExist:
            await self.send_error(f"Task not found: {task_id}")
            return

        # Verify task belongs to agent's project
        if task.project != self.agent.project:
            await self.send_error("Task does not belong to agent's project")
            return

        # Start execution
        self.execution_task = asyncio.create_task(
            self.execute_agent_task(task)
        )

    async def handle_user_input(self, response: str):
        """Handle user input response."""
        # In a full implementation, this would send input to the waiting agent
        await self.send_event({
            'type': 'user_input_received',
            'content': response,
        })

    async def handle_cancel(self):
        """Handle execution cancellation."""
        if self.execution_task and not self.execution_task.done():
            self.execution_task.cancel()
            await self.send_event({
                'type': 'cancelled',
                'message': 'Execution cancelled by user',
            })
        else:
            await self.send_error("No active execution to cancel")

    async def execute_agent_task(self, task: Task):
        """Execute agent task and stream events."""
        try:
            # Create runtime
            runtime = AgentRuntime(self.agent)

            # Execute task and stream events
            async for event in runtime.execute_task(task):
                # Send event to WebSocket
                await self.send_event(event)

            # Send done event
            await self.send_event({
                'type': 'done',
                'task_id': str(task.id),
            })

        except asyncio.CancelledError:
            await self.send_event({
                'type': 'cancelled',
                'message': 'Execution was cancelled',
            })
        except Exception as e:
            await self.send_event({
                'type': 'error',
                'error': str(e),
                'recoverable': False,
            })

    async def send_event(self, event: Dict[str, Any]):
        """Send event to WebSocket with optimized JSON serialization."""
        if USE_ORJSON:
            # orjson is 2-3x faster than standard json
            text_data = orjson.dumps(event).decode('utf-8')
        else:
            text_data = json.dumps(event)
        await self.send(text_data=text_data)

    async def send_error(self, error: str):
        """Send error event."""
        await self.send_event({
            'type': 'error',
            'error': error,
            'recoverable': True,
        })

    # Database operations (sync_to_async wrapped)

    @database_sync_to_async
    def get_agent(self, agent_id):
        """Get agent from database."""
        return AgentInstance.objects.select_related(
            'agent_type', 'project'
        ).get(id=agent_id)

    @database_sync_to_async
    def get_task(self, task_id):
        """Get task from database."""
        return Task.objects.select_related('project').get(id=task_id)


class ProjectChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for multi-agent conversations.

    Handles real-time multi-agent conversations where agents discuss
    requirements, architecture, and implementation in front of the user.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_id = None
        self.user_id = None
        self.conversation_orchestrator = None
        self.conversation_task = None

    async def connect(self):
        """Handle WebSocket connection."""
        # Get project ID from URL
        self.project_id = self.scope['url_route']['kwargs']['project_id']

        # Get user from scope
        user = self.scope.get('user')

        # Authenticate - check if user is anonymous by type name to avoid lazy loading
        if not user or user.__class__.__name__ == 'AnonymousUser':
            await self.close(code=4001)
            return

        # Store only user ID to avoid ORM lazy loading issues
        self.user_id = user.id

        # Verify project exists and user has access
        try:
            project_data = await self.verify_project_access(self.project_id, self.user_id)
            if not project_data:
                await self.close(code=4003)
                return
        except ObjectDoesNotExist:
            await self.close(code=4004)
            return

        # Accept connection
        await self.accept()

        # Send connection success immediately (don't block on agent initialization)
        await self.send_event({
            'type': 'connected',
            'project_id': str(self.project_id),
            'project_name': project_data['name'],
            'message': 'Connected! Start chatting with Alex and the team.',
        })

        # Initialize conversation orchestrator in background (lazy initialization)
        from apps.agents.engine.conversation_orchestrator import ConversationOrchestrator
        project = await self.get_project_for_orchestrator()
        self.conversation_orchestrator = ConversationOrchestrator(project)
        # Don't await - let it initialize in background
        asyncio.create_task(self.conversation_orchestrator.initialize_agents())

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
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

            if message_type == 'message':
                # User sent a message
                message_content = data.get('content', '')
                if message_content:
                    await self.handle_user_message(message_content)
                else:
                    await self.send_error("Empty message")

            elif message_type == 'ping':
                await self.send_event({'type': 'pong'})

            else:
                await self.send_error(f"Unknown message type: {message_type}")

        except json.JSONDecodeError:
            await self.send_error("Invalid JSON")
        except Exception as e:
            await self.send_error(f"Error: {str(e)}")

    async def handle_user_message(self, message: str):
        """Handle user message and start multi-agent conversation."""
        if not message.strip():
            await self.send_error("Empty message")
            return

        if not self.conversation_orchestrator:
            await self.send_error("Conversation not initialized")
            return

        # Wait for agents to be initialized (max 10 seconds)
        max_wait = 100  # 10 seconds (100 * 0.1s)
        wait_count = 0
        while not self.conversation_orchestrator.active_agents and wait_count < max_wait:
            await asyncio.sleep(0.1)
            wait_count += 1

        if not self.conversation_orchestrator.active_agents:
            await self.send_error("Agents failed to initialize")
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

    async def send_event(self, event: Dict[str, Any]):
        """Send event to WebSocket."""
        if USE_ORJSON:
            text_data = orjson.dumps(event).decode('utf-8')
        else:
            text_data = json.dumps(event)
        await self.send(text_data=text_data)

    async def send_error(self, error: str):
        """Send error event."""
        await self.send_event({
            'type': 'error',
            'content': error,
        })

    # Database operations

    @database_sync_to_async
    def verify_project_access(self, project_id, user_id):
        """Verify project exists and user has access."""
        from apps.projects.models import Project
        try:
            project = Project.objects.get(id=project_id, owner_id=user_id)
            return {
                'id': str(project.id),
                'name': project.name,
            }
        except Project.DoesNotExist:
            return None

    @database_sync_to_async
    def get_project_for_orchestrator(self):
        """Get project object for conversation orchestrator."""
        from apps.projects.models import Project
        return Project.objects.get(id=self.project_id)
