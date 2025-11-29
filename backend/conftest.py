"""
Root conftest.py for pytest configuration.

Provides fixtures and configuration for all tests.
"""
import pytest
from typing import Generator
from django.conf import settings
from django.test import Client
from rest_framework.test import APIClient
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
import asyncio

# Import factories
from apps.accounts.tests.factories import UserFactory
from apps.projects.tests.factories import ProjectFactory
from apps.agents.tests.factories import AgentTypeFactory, AgentInstanceFactory
from apps.tasks.tests.factories import TaskFactory


# ============================================================================
# Django & DRF Fixtures
# ============================================================================

@pytest.fixture(scope='function')
def client():
    """Django test client."""
    return Client()


@pytest.fixture(scope='function')
def api_client():
    """DRF API client."""
    return APIClient()


@pytest.fixture(scope='function')
def authenticated_client(api_client, user):
    """Authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client


# ============================================================================
# Model Fixtures
# ============================================================================

@pytest.fixture
def user(db):
    """Create a test user."""
    return UserFactory()


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return UserFactory(is_staff=True, is_superuser=True)


@pytest.fixture
def project(db, user):
    """Create a test project."""
    return ProjectFactory(owner=user)


@pytest.fixture
def agent_type(db):
    """Create an agent type."""
    return AgentTypeFactory()


@pytest.fixture
def orchestrator_type(db):
    """Create orchestrator agent type."""
    return AgentTypeFactory(
        name="Orchestrator",
        role="orchestrator",
        hierarchy_level=0
    )


@pytest.fixture
def agent_instance(db, project, agent_type):
    """Create an agent instance."""
    return AgentInstanceFactory(project=project, agent_type=agent_type)


@pytest.fixture
def task(db, project):
    """Create a task."""
    return TaskFactory(project=project)


# ============================================================================
# WebSocket Fixtures
# ============================================================================

@pytest.fixture
async def channel_layer():
    """Get channel layer for WebSocket tests."""
    return get_channel_layer()


@pytest.fixture
async def websocket_communicator(project, user):
    """Create WebSocket communicator."""
    from apps.projects.consumers import ProjectExecutionConsumer

    communicator = WebsocketCommunicator(
        ProjectExecutionConsumer.as_asgi(),
        f"/ws/projects/{project.id}/stream/"
    )

    # Add user to scope
    communicator.scope['user'] = user

    return communicator


# ============================================================================
# Database Fixtures
# ============================================================================

@pytest.fixture(scope='function')
def db_with_data(db, user, project, agent_type, agent_instance, task):
    """Database with full test data."""
    return {
        'user': user,
        'project': project,
        'agent_type': agent_type,
        'agent_instance': agent_instance,
        'task': task,
    }


# ============================================================================
# Mock Fixtures
# ============================================================================

@pytest.fixture
def mock_ollama_response():
    """Mock Ollama API response."""
    return {
        "model": "deepseek-r1:7b",
        "created_at": "2025-01-01T00:00:00Z",
        "response": "I'll help you with that task.",
        "done": True,
        "context": [],
        "total_duration": 1000000000,
        "load_duration": 500000000,
        "prompt_eval_count": 10,
        "eval_count": 20,
    }


@pytest.fixture
def mock_llm_client(mocker, mock_ollama_response):
    """Mock LLM client."""
    mock_client = mocker.Mock()
    mock_client.generate.return_value = mock_ollama_response
    return mock_client


# ============================================================================
# Async Fixtures
# ============================================================================

@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# Cleanup Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def clear_cache():
    """Clear cache before each test."""
    from django.core.cache import cache
    cache.clear()
    yield
    cache.clear()


@pytest.fixture(autouse=True)
def reset_sequences(db):
    """Reset database sequences after each test."""
    yield
    # Sequences are automatically reset by Django's TestCase


# ============================================================================
# Settings Fixtures
# ============================================================================

@pytest.fixture
def settings_with_test_config(settings):
    """Settings with test configuration."""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True
    return settings
