"""
Checkpoint API Views

Project checkpoint management endpoints.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.projects.models import Project, ProjectCheckpoint
from apps.projects.serializers import (
    ProjectCheckpointSerializer,
    ProjectCheckpointListSerializer,
)
from apps.agents.models import AgentInstance
from apps.tasks.models import Task, TaskStatus


class ProjectCheckpointListView(APIView):
    """
    Project checkpoint list endpoint.

    GET /api/projects/{id}/checkpoints/ - List checkpoints
    POST /api/projects/{id}/checkpoints/ - Create checkpoint
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """List project checkpoints."""
        try:
            project = Project.objects.get(id=pk, owner=request.user)
        except Project.DoesNotExist:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)

        checkpoints = ProjectCheckpoint.objects.filter(
            project=project
        ).order_by('-created_at')

        serializer = ProjectCheckpointListSerializer(checkpoints, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        """Create project checkpoint."""
        try:
            project = Project.objects.get(id=pk, owner=request.user)
        except Project.DoesNotExist:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Build state snapshot
        state_snapshot = {
            'project_status': project.status,
            'manifest': project.manifest,
            'agents': list(AgentInstance.objects.filter(project=project).values(
                'id', 'agent_type__name', 'status', 'working_memory'
            )),
            'tasks_summary': {
                'total': Task.objects.filter(project=project).count(),
                'completed': Task.objects.filter(project=project, status=TaskStatus.COMPLETED).count(),
                'pending': Task.objects.filter(project=project, status__in=[TaskStatus.TODO, TaskStatus.BACKLOG, TaskStatus.ASSIGNED]).count()
            }
        }

        checkpoint_data = {
            'project': str(project.id),
            'name': request.data.get('name', f'Checkpoint {ProjectCheckpoint.objects.filter(project=project).count() + 1}'),
            'description': request.data.get('description', ''),
            'state_snapshot': state_snapshot,
            'created_by': str(request.user.id),
            'is_auto': False
        }

        serializer = ProjectCheckpointSerializer(data=checkpoint_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectCheckpointDetailView(APIView):
    """
    Project checkpoint detail endpoint.

    GET /api/projects/{project_id}/checkpoints/{id}/ - Get checkpoint
    DELETE /api/projects/{project_id}/checkpoints/{id}/ - Delete checkpoint
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, checkpoint_id):
        """Get checkpoint details."""
        try:
            checkpoint = ProjectCheckpoint.objects.get(
                id=checkpoint_id,
                project_id=project_id,
                project__owner=request.user
            )
        except ProjectCheckpoint.DoesNotExist:
            return Response({
                'error': 'Checkpoint not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectCheckpointSerializer(checkpoint)
        return Response(serializer.data)

    def delete(self, request, project_id, checkpoint_id):
        """Delete checkpoint."""
        try:
            checkpoint = ProjectCheckpoint.objects.get(
                id=checkpoint_id,
                project_id=project_id,
                project__owner=request.user
            )
        except ProjectCheckpoint.DoesNotExist:
            return Response({
                'error': 'Checkpoint not found'
            }, status=status.HTTP_404_NOT_FOUND)

        checkpoint.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
