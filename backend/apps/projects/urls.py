"""
URLs for projects app.
"""

from django.urls import path
from .views import (
    ProjectListView,
    ProjectDetailView,
    ProjectStatusView,
    ProjectCheckpointListView,
    ProjectCheckpointDetailView
)

app_name = 'projects'

urlpatterns = [
    # Projects
    path('', ProjectListView.as_view(), name='project-list'),
    path('<uuid:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<uuid:pk>/status/', ProjectStatusView.as_view(), name='project-status'),

    # Agents (delegate to agents app)
    path('<uuid:project_id>/agents/', lambda request, project_id: __import__('apps.agents.views', fromlist=['AgentListView']).AgentListView.as_view()(request, project_id=project_id)),

    # Tasks (delegate to tasks app)
    path('<uuid:project_id>/tasks/', lambda request, project_id: __import__('apps.tasks.views', fromlist=['TaskListView']).TaskListView.as_view()(request, project_id=project_id)),

    # Checkpoints
    path('<uuid:pk>/checkpoints/', ProjectCheckpointListView.as_view(), name='checkpoint-list'),
    path('<uuid:project_id>/checkpoints/<uuid:checkpoint_id>/', ProjectCheckpointDetailView.as_view(), name='checkpoint-detail'),
]
