"""
Checkpoint Serializers

Serializers for the ProjectCheckpoint model.
"""

from rest_framework import serializers
from apps.projects.models import ProjectCheckpoint


class ProjectCheckpointSerializer(serializers.ModelSerializer):
    """Serializer for ProjectCheckpoint model."""

    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = ProjectCheckpoint
        fields = [
            'id', 'project', 'project_name', 'name', 'description',
            'state_snapshot', 'created_by', 'is_auto',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        """Validate checkpoint name is unique for project."""
        project = self.initial_data.get('project')
        if ProjectCheckpoint.objects.filter(project=project, name=value).exists():
            if not self.instance or self.instance.name != value:
                raise serializers.ValidationError(
                    "A checkpoint with this name already exists for this project."
                )
        return value


class ProjectCheckpointListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for checkpoint lists."""

    class Meta:
        model = ProjectCheckpoint
        fields = [
            'id', 'name', 'description', 'is_auto', 'created_at'
        ]
        read_only_fields = fields
