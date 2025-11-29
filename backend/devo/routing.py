"""
WebSocket routing configuration for DEVO.

Defines WebSocket URL patterns and routes to consumers.
"""
from django.urls import path, re_path

from apps.projects.consumers import ProjectExecutionConsumer
from apps.agents.consumers import AgentExecutionConsumer, ProjectChatConsumer

websocket_urlpatterns = [
    # Project execution WebSocket
    path('ws/projects/<uuid:project_id>/stream/', ProjectExecutionConsumer.as_asgi()),

    # Project chat WebSocket (with history persistence)
    path('ws/projects/<uuid:project_id>/chat/', ProjectChatConsumer.as_asgi()),

    # Agent execution WebSocket
    path('ws/agents/<uuid:agent_id>/execute/', AgentExecutionConsumer.as_asgi()),
]
