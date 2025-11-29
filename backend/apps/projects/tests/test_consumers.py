"""
Tests for WebSocket consumers.
"""
import pytest
import json
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async

from apps.projects.consumers import ProjectExecutionConsumer
from apps.projects.tests.factories import ProjectFactory
from apps.accounts.tests.factories import UserFactory
from apps.agents.tests.factories import AgentTypeFactory


@pytest.mark.django_db
@pytest.mark.asyncio
class TestProjectExecutionConsumer:
    """Tests for ProjectExecutionConsumer."""

    async def test_websocket_connect_authenticated(self):
        """Test WebSocket connection with authenticated user."""
        user = await database_sync_to_async(UserFactory)()
        project = await database_sync_to_async(ProjectFactory)(owner=user)

        communicator = WebsocketCommunicator(
            ProjectExecutionConsumer.as_asgi(),
            f"/ws/projects/{project.id}/stream/"
        )
        communicator.scope['user'] = user

        connected, _ = await communicator.connect()
        assert connected is True

        # Receive connection success message
        response = await communicator.receive_json_from()
        assert response['type'] == 'connected'
        assert response['project_id'] == str(project.id)

        await communicator.disconnect()

    async def test_websocket_connect_unauthenticated(self):
        """Test WebSocket connection without authentication."""
        from django.contrib.auth.models import AnonymousUser

        project = await database_sync_to_async(ProjectFactory)()

        communicator = WebsocketCommunicator(
            ProjectExecutionConsumer.as_asgi(),
            f"/ws/projects/{project.id}/stream/"
        )
        communicator.scope['user'] = AnonymousUser()

        connected, close_code = await communicator.connect()
        assert connected is False
        assert close_code == 4001  # Unauthorized

    async def test_websocket_connect_wrong_owner(self):
        """Test WebSocket connection with wrong owner."""
        user = await database_sync_to_async(UserFactory)()
        other_user = await database_sync_to_async(UserFactory)()
        project = await database_sync_to_async(ProjectFactory)(owner=other_user)

        communicator = WebsocketCommunicator(
            ProjectExecutionConsumer.as_asgi(),
            f"/ws/projects/{project.id}/stream/"
        )
        communicator.scope['user'] = user

        connected, close_code = await communicator.connect()
        assert connected is False
        assert close_code == 4003  # Forbidden

    async def test_user_message_handling(self):
        """Test handling user message."""
        user = await database_sync_to_async(UserFactory)()
        project = await database_sync_to_async(ProjectFactory)(owner=user)

        # Create orchestrator agent type
        await database_sync_to_async(AgentTypeFactory)(
            name="Orchestrator",
            role="orchestrator",
            hierarchy_level=0
        )

        communicator = WebsocketCommunicator(
            ProjectExecutionConsumer.as_asgi(),
            f"/ws/projects/{project.id}/stream/"
        )
        communicator.scope['user'] = user

        connected, _ = await communicator.connect()
        assert connected is True

        # Receive connection message
        await communicator.receive_json_from()

        # Send user message
        await communicator.send_json_to({
            'type': 'user_message',
            'content': 'Test message'
        })

        # Should receive some response (exact response depends on implementation)
        # For now, just verify no errors
        await communicator.disconnect()

    async def test_cancel_execution(self):
        """Test cancelling execution."""
        user = await database_sync_to_async(UserFactory)()
        project = await database_sync_to_async(ProjectFactory)(owner=user)

        communicator = WebsocketCommunicator(
            ProjectExecutionConsumer.as_asgi(),
            f"/ws/projects/{project.id}/stream/"
        )
        communicator.scope['user'] = user

        connected, _ = await communicator.connect()
        assert connected is True

        # Receive connection message
        await communicator.receive_json_from()

        # Send cancel message
        await communicator.send_json_to({
            'type': 'cancel'
        })

        # Should receive error (no active execution)
        response = await communicator.receive_json_from()
        assert response['type'] == 'error'

        await communicator.disconnect()

    async def test_invalid_message_type(self):
        """Test handling invalid message type."""
        user = await database_sync_to_async(UserFactory)()
        project = await database_sync_to_async(ProjectFactory)(owner=user)

        communicator = WebsocketCommunicator(
            ProjectExecutionConsumer.as_asgi(),
            f"/ws/projects/{project.id}/stream/"
        )
        communicator.scope['user'] = user

        connected, _ = await communicator.connect()
        assert connected is True

        # Receive connection message
        await communicator.receive_json_from()

        # Send invalid message type
        await communicator.send_json_to({
            'type': 'invalid_type'
        })

        # Should receive error
        response = await communicator.receive_json_from()
        assert response['type'] == 'error'

        await communicator.disconnect()
