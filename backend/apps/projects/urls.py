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
    # Projects CRUD
    # GET /api/projects/ - List all projects
    # POST /api/projects/ - Create new project
    path('', ProjectListView.as_view(), name='project-list'),
    
    # GET /api/projects/{id}/ - Get project details
    # PATCH /api/projects/{id}/ - Update project
    # DELETE /api/projects/{id}/ - Delete project
    path('<uuid:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    
    # Additional endpoints
    path('<uuid:pk>/status/', ProjectStatusView.as_view(), name='project-status'),
    path('<uuid:pk>/checkpoints/', ProjectCheckpointListView.as_view(), name='checkpoint-list'),
    path('<uuid:project_id>/checkpoints/<uuid:checkpoint_id>/', ProjectCheckpointDetailView.as_view(), name='checkpoint-detail'),
]
