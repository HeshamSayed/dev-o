"""
Project Serializers

Serializers for projects and project checkpoints.
"""

from rest_framework import serializers
from .models import Project, ProjectCheckpoint


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model."""

    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    agent_count = serializers.SerializerMethodField()
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status', 'owner',
            'owner_email', 'local_path', 'repository_url',
            'manifest', 'agent_count', 'task_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def get_agent_count(self, obj):
        """Get number of agents in project."""
        return obj.agents.count()

    def get_task_count(self, obj):
        """Get number of tasks in project."""
        return obj.tasks.count()

    def validate_name(self, value):
        """Validate project name is unique for user."""
        user = self.context['request'].user
        if Project.objects.filter(owner=user, name=value).exists():
            if not self.instance or self.instance.name != value:
                raise serializers.ValidationError(
                    "You already have a project with this name."
                )
        return value


class ProjectDetailSerializer(ProjectSerializer):
    """Detailed project serializer with additional info."""

    agents = serializers.SerializerMethodField()
    recent_tasks = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + [
            'agents', 'recent_tasks', 'statistics'
        ]

    def get_agents(self, obj):
        """Get list of agents in project."""
        from apps.agents.serializers import AgentInstanceListSerializer
        agents = obj.agents.select_related('agent_type').all()
        return AgentInstanceListSerializer(agents, many=True).data

    def get_recent_tasks(self, obj):
        """Get recent tasks."""
        from apps.tasks.serializers import TaskListSerializer
        tasks = obj.tasks.select_related(
            'assigned_to'
        ).order_by('-created_at')[:10]
        return TaskListSerializer(tasks, many=True).data

    def get_statistics(self, obj):
        """Get project statistics."""
        from apps.agents.models import AgentInstance
        from apps.tasks.models import Task, TaskStatus

        return {
            'total_agents': AgentInstance.objects.filter(project=obj).count(),
            'total_tasks': Task.objects.filter(project=obj).count(),
            'completed_tasks': Task.objects.filter(
                project=obj,
                status=TaskStatus.COMPLETED
            ).count(),
            'pending_tasks': Task.objects.filter(
                project=obj,
                status__in=[TaskStatus.TODO, TaskStatus.BACKLOG, TaskStatus.ASSIGNED]
            ).count(),
            'files_created': obj.code_artifacts.count()
        }


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


class ProjectCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating projects."""

    class Meta:
        model = Project
        fields = [
            'name', 'description', 'local_path', 'repository_url'
        ]

    def create(self, validated_data):
        """Create project and initialize orchestrator."""
        user = self.context['request'].user
        project = Project.objects.create(
            owner=user,
            status='initializing',
            **validated_data
        )

        # Initialize manifest
        project.manifest = {
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat(),
            "tech_stack": {},
            "architecture": {},
            "domain_model": {},
            "requirements": {}
        }
        project.save()

        # Log project creation event
        from apps.context.services.event_store import EventStore
        EventStore.log_project_created(project, str(user.id))

        return project


class ProjectStatusSerializer(serializers.Serializer):
    """Serializer for project status endpoint."""

    status = serializers.CharField()
    active_agents = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    recent_activity = serializers.ListField()
