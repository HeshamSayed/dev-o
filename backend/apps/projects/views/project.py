"""
Project API Views

Project management endpoints.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.projects.models import Project
from apps.projects.serializers import (
    ProjectSerializer,
    ProjectDetailSerializer,
    ProjectCreateSerializer,
    ProjectStatusSerializer,
)
from apps.agents.models import AgentInstance, AgentStatus
from apps.tasks.models import Task, TaskStatus


class ProjectListView(APIView):
    """
    Project list endpoint.

    GET /api/projects/ - List user's projects
    POST /api/projects/ - Create new project
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List user's projects."""
        projects = Project.objects.filter(
            owner=request.user
        ).order_by('-created_at')

        serializer = ProjectSerializer(projects, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        """Create new project."""
        # Check subscription limits
        user_projects = Project.objects.filter(owner=request.user).count()
        
        # Get max_projects from subscription (default to 1 for free tier if no subscription)
        try:
            max_projects = request.user.subscription.max_projects
        except:
            max_projects = 1  # Default free tier limit

        # -1 means unlimited
        if max_projects >= 0 and user_projects >= max_projects:
            return Response({
                'error': f'Maximum project limit reached ({max_projects}). Upgrade subscription.'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = ProjectCreateSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            project = serializer.save()
            return Response(
                ProjectDetailSerializer(project, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    """
    Project detail endpoint.

    GET /api/projects/{id}/ - Get project details
    PATCH /api/projects/{id}/ - Update project
    DELETE /api/projects/{id}/ - Delete project
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        """Get project if user has access."""
        try:
            return Project.objects.get(id=pk, owner=request.user)
        except Project.DoesNotExist:
            return None

    def get(self, request, pk):
        """Get project details."""
        project = self.get_object(request, pk)

        if not project:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectDetailSerializer(project, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        """Update project."""
        project = self.get_object(request, pk)

        if not project:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(
            project,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete project."""
        project = self.get_object(request, pk)

        if not project:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)

        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectStatusView(APIView):
    """
    Project status endpoint.

    GET /api/projects/{id}/status/ - Get real-time project status
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get project status."""
        try:
            project = Project.objects.get(id=pk, owner=request.user)
        except Project.DoesNotExist:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Get active agents
        active_agents = AgentInstance.objects.filter(
            project=project,
            status__in=[AgentStatus.WORKING, AgentStatus.WAITING_INPUT]
        ).count()

        # Get task counts
        pending_tasks = Task.objects.filter(
            project=project,
            status__in=[TaskStatus.TODO, TaskStatus.BACKLOG, TaskStatus.ASSIGNED]
        ).count()

        completed_tasks = Task.objects.filter(
            project=project,
            status=TaskStatus.COMPLETED
        ).count()

        # Get recent activity
        from apps.context.services.event_store import EventStore
        recent_events = EventStore.get_project_timeline(project, limit=10)

        data = {
            'status': project.status,
            'active_agents': active_agents,
            'pending_tasks': pending_tasks,
            'completed_tasks': completed_tasks,
            'recent_activity': recent_events
        }

        serializer = ProjectStatusSerializer(data)
        return Response(serializer.data)
