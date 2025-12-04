"""Project views."""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import zipfile
import io

from .models import Project, ProjectFile
from .serializers import (
    ProjectSerializer,
    ProjectFileSerializer,
    CreateProjectSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for managing projects."""

    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateProjectSerializer
        return ProjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        # Return full project data
        output_serializer = ProjectSerializer(project)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def files(self, request, pk=None):
        """List all files in a project."""
        project = self.get_object()
        files = project.files.all()
        serializer = ProjectFileSerializer(files, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='files/(?P<file_path>.+)')
    def file_content(self, request, pk=None, file_path=None):
        """Get specific file content."""
        project = self.get_object()
        try:
            file = project.files.get(path=file_path)
            serializer = ProjectFileSerializer(file)
            return Response(serializer.data)
        except ProjectFile.DoesNotExist:
            return Response(
                {'error': 'File not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download project as ZIP file."""
        project = self.get_object()
        files = project.files.all()

        # Create ZIP in memory
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in files:
                zf.writestr(file.path, file.content)

        buffer.seek(0)

        response = HttpResponse(buffer.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{project.name}.zip"'
        return response

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark project as completed."""
        project = self.get_object()
        project.status = 'completed'
        project.save()
        return Response({'status': 'completed'})
