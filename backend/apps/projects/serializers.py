"""Project serializers."""

from rest_framework import serializers
from .models import Project, ProjectFile


class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ['id', 'path', 'content', 'language', 'version', 'created_at', 'updated_at']
        read_only_fields = ['id', 'version', 'created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    file_count = serializers.SerializerMethodField()
    file_tree = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'project_type', 'status',
            'file_count', 'file_tree', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def get_file_count(self, obj):
        return obj.files.count()

    def get_file_tree(self, obj):
        return obj.get_file_tree()


class CreateProjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    project_type = serializers.ChoiceField(choices=Project.PROJECT_TYPES)

    def create(self, validated_data):
        user = self.context['request'].user

        # Create project (CrewAI handles agents internally)
        project = Project.objects.create(
            user=user,
            name=validated_data['name'],
            description=validated_data.get('description', ''),
            project_type=validated_data['project_type']
        )

        return project
