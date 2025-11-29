"""
Task API Views

Task management endpoints.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskListSerializer
from apps.projects.models import Project


class TaskListView(APIView):
    """
    Task list endpoint.

    GET /api/projects/{project_id}/tasks/ - List project's tasks
    POST /api/projects/{project_id}/tasks/ - Create new task
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """List project's tasks."""
        try:
            project = Project.objects.get(id=project_id, owner=request.user)
        except Project.DoesNotExist:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Get filter params
        status_filter = request.query_params.get('status')

        tasks = Task.objects.filter(project=project).select_related(
            'assigned_to', 'parent_task'
        ).order_by('-created_at')

        if status_filter:
            tasks = tasks.filter(status=status_filter)

        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        """Create new task."""
        try:
            project = Project.objects.get(id=project_id, owner=request.user)
        except Project.DoesNotExist:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Add project to request data
        data = request.data.copy()
        data['project'] = str(project.id)

        from .serializers import TaskCreateSerializer
        serializer = TaskCreateSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            task = serializer.save()
            return Response(
                TaskListSerializer(task).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
