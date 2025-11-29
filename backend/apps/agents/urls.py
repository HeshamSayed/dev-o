"""
URLs for agents app.
"""

from django.urls import path
from .views import (
    AgentTypeListView,
    AgentTypeDetailView,
    AgentListView,
    AgentHireView,
    AgentDetailView,
    AgentMessagesView,
    AgentActionsView,
    AgentExecuteView,
    ProjectExecuteView
)

app_name = 'agents'

urlpatterns = [
    # Agent Types
    path('agent-types/', AgentTypeListView.as_view(), name='agent-type-list'),
    path('agent-types/<uuid:pk>/', AgentTypeDetailView.as_view(), name='agent-type-detail'),

    # Project Agents
    path('projects/<uuid:project_id>/agents/', AgentListView.as_view(), name='agent-list'),
    path('projects/<uuid:project_id>/agents/hire/', AgentHireView.as_view(), name='agent-hire'),

    # Agent Management
    path('<uuid:pk>/', AgentDetailView.as_view(), name='agent-detail'),
    path('<uuid:pk>/messages/', AgentMessagesView.as_view(), name='agent-messages'),
    path('<uuid:pk>/actions/', AgentActionsView.as_view(), name='agent-actions'),
    path('<uuid:pk>/execute/', AgentExecuteView.as_view(), name='agent-execute'),

    # Project Execution
    path('projects/<uuid:project_id>/execute/', ProjectExecuteView.as_view(), name='project-execute'),
]
