"""
Code Serializers

Serializers for code artifacts, changes, and artifact registry.
"""

from rest_framework import serializers
from .models import CodeArtifact, CodeChange, ArtifactRegistry


class CodeArtifactSerializer(serializers.ModelSerializer):
    """Serializer for CodeArtifact model."""

    project_name = serializers.CharField(source='project.name', read_only=True)
    created_by_name = serializers.CharField(
        source='created_by_agent.agent_type.name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = CodeArtifact
        fields = [
            'id', 'project', 'project_name', 'file_path', 'content',
            'content_hash', 'language', 'structure', 'embedding',
            'created_by_agent', 'created_by_name', 'created_by_task',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'content_hash', 'embedding', 'created_at', 'updated_at'
        ]


class CodeArtifactListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for code artifact lists."""

    class Meta:
        model = CodeArtifact
        fields = [
            'id', 'file_path', 'language', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = fields


class CodeArtifactCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating code artifacts."""

    class Meta:
        model = CodeArtifact
        fields = [
            'file_path', 'content', 'language', 'structure'
        ]

    def create(self, validated_data):
        """Create code artifact."""
        import hashlib

        # Calculate content hash
        content = validated_data['content']
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        artifact = CodeArtifact.objects.create(
            project=self.context['project'],
            created_by_agent=self.context.get('created_by_agent'),
            created_by_task=self.context.get('created_by_task'),
            content_hash=content_hash,
            **validated_data
        )

        return artifact


class CodeChangeSerializer(serializers.ModelSerializer):
    """Serializer for CodeChange model."""

    artifact_path = serializers.CharField(source='artifact.file_path', read_only=True)
    agent_name = serializers.CharField(
        source='agent.agent_type.name',
        read_only=True,
        allow_null=True
    )
    task_title = serializers.CharField(
        source='task.title',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = CodeChange
        fields = [
            'id', 'artifact', 'artifact_path', 'change_type', 'diff',
            'description', 'agent', 'agent_name', 'task', 'task_title',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CodeChangeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for code change lists."""

    artifact_path = serializers.CharField(source='artifact.file_path', read_only=True)
    agent_name = serializers.CharField(
        source='agent.agent_type.name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = CodeChange
        fields = [
            'id', 'artifact_path', 'change_type', 'agent_name', 'created_at'
        ]
        read_only_fields = fields


class ArtifactRegistrySerializer(serializers.ModelSerializer):
    """Serializer for ArtifactRegistry model."""

    project_name = serializers.CharField(source='project.name', read_only=True)
    created_by_name = serializers.CharField(
        source='created_by_agent.agent_type.name',
        read_only=True,
        allow_null=True
    )
    task_title = serializers.CharField(
        source='created_by_task.title',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = ArtifactRegistry
        fields = [
            'id', 'project', 'project_name', 'artifact_type', 'name',
            'file_path', 'line_start', 'line_end', 'details',
            'dependencies', 'embedding', 'created_by_agent',
            'created_by_name', 'created_by_task', 'task_title',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'embedding', 'created_at', 'updated_at']


class ArtifactRegistryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for artifact registry lists."""

    class Meta:
        model = ArtifactRegistry
        fields = [
            'id', 'artifact_type', 'name', 'file_path',
            'is_active', 'created_at'
        ]
        read_only_fields = fields


class ArtifactRegistryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating artifact registry entries."""

    class Meta:
        model = ArtifactRegistry
        fields = [
            'artifact_type', 'name', 'file_path', 'line_start',
            'line_end', 'details', 'dependencies'
        ]

    def create(self, validated_data):
        """Create artifact registry entry."""
        artifact = ArtifactRegistry.objects.create(
            project=self.context['project'],
            created_by_agent=self.context.get('created_by_agent'),
            created_by_task=self.context.get('created_by_task'),
            **validated_data
        )

        return artifact


class ArtifactRegistryDetailSerializer(ArtifactRegistrySerializer):
    """Detailed artifact registry serializer with dependencies."""

    dependency_artifacts = serializers.SerializerMethodField()
    dependent_artifacts = serializers.SerializerMethodField()

    class Meta(ArtifactRegistrySerializer.Meta):
        fields = ArtifactRegistrySerializer.Meta.fields + [
            'dependency_artifacts', 'dependent_artifacts'
        ]

    def get_dependency_artifacts(self, obj):
        """Get artifacts this depends on."""
        if not obj.dependencies:
            return []

        deps = ArtifactRegistry.objects.filter(
            id__in=obj.dependencies,
            is_active=True
        )
        return ArtifactRegistryListSerializer(deps, many=True).data

    def get_dependent_artifacts(self, obj):
        """Get artifacts that depend on this."""
        dependents = ArtifactRegistry.objects.filter(
            dependencies__contains=[str(obj.id)],
            is_active=True
        )
        return ArtifactRegistryListSerializer(dependents, many=True).data


class FileContentSerializer(serializers.Serializer):
    """Serializer for file content requests."""

    file_path = serializers.CharField()
    content = serializers.CharField(read_only=True)
    language = serializers.CharField(read_only=True)
    lines = serializers.IntegerField(read_only=True)
