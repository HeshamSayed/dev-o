"""
Task Serializers

Serializers for tasks, dependencies, and logs.
"""

from rest_framework import serializers
from .models import Task, TaskDependency, TaskLog, TaskStatus, TaskPriority


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""

    project_name = serializers.CharField(source='project.name', read_only=True)
    assigned_to_name = serializers.CharField(
        source='assigned_to_agent.agent_type.name',
        read_only=True,
        allow_null=True
    )
    created_by_name = serializers.CharField(
        source='created_by_agent.agent_type.name',
        read_only=True,
        allow_null=True
    )
    parent_task_title = serializers.CharField(
        source='parent_task.title',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'project_name', 'title', 'description',
            'task_type', 'priority', 'status', 'assigned_to_agent',
            'assigned_to_name', 'created_by_agent', 'created_by_name',
            'parent_task', 'parent_task_title', 'requirements',
            'acceptance_criteria', 'deliverables', 'completion_summary',
            'iteration_count', 'estimated_complexity', 'created_at',
            'updated_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'created_by_agent', 'iteration_count',
            'created_at', 'updated_at', 'completed_at'
        ]


class TaskListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for task lists."""

    assigned_to_name = serializers.CharField(
        source='assigned_to_agent.agent_type.name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'task_type', 'priority', 'status',
            'assigned_to_name', 'created_at'
        ]
        read_only_fields = fields


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks."""

    class Meta:
        model = Task
        fields = [
            'title', 'description', 'task_type', 'priority',
            'assigned_to_agent', 'parent_task', 'requirements',
            'acceptance_criteria', 'estimated_complexity'
        ]

    def create(self, validated_data):
        """Create task."""
        task = Task.objects.create(
            project=self.context['project'],
            created_by_agent=self.context.get('created_by_agent'),
            **validated_data
        )

        # Log event
        from apps.context.services.event_store import EventStore
        EventStore.log_task_created(
            project=task.project,
            task_id=str(task.id),
            task_title=task.title,
            created_by=str(self.context.get('created_by_agent').id) if self.context.get('created_by_agent') else 'user'
        )

        return task


class TaskUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating tasks."""

    class Meta:
        model = Task
        fields = [
            'title', 'description', 'priority', 'status',
            'assigned_to_agent', 'requirements', 'acceptance_criteria',
            'deliverables', 'completion_summary'
        ]

    def update(self, instance, validated_data):
        """Update task and log changes."""
        old_status = instance.status
        new_status = validated_data.get('status', old_status)

        # Update task
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle completion
        if new_status == TaskStatus.COMPLETED and old_status != TaskStatus.COMPLETED:
            from datetime import datetime
            instance.completed_at = datetime.now()

            # Log completion event
            from apps.context.services.event_store import EventStore
            EventStore.log_task_completed(
                project=instance.project,
                task_id=str(instance.id),
                task_title=instance.title,
                completed_by=str(instance.assigned_to_agent.id) if instance.assigned_to_agent else 'unknown'
            )

        instance.save()
        return instance


class TaskDependencySerializer(serializers.ModelSerializer):
    """Serializer for TaskDependency model."""

    task_title = serializers.CharField(source='task.title', read_only=True)
    depends_on_title = serializers.CharField(source='depends_on.title', read_only=True)
    depends_on_status = serializers.CharField(source='depends_on.status', read_only=True)

    class Meta:
        model = TaskDependency
        fields = [
            'id', 'task', 'task_title', 'depends_on', 'depends_on_title',
            'depends_on_status', 'dependency_type', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        """Validate no circular dependencies."""
        task = attrs.get('task')
        depends_on = attrs.get('depends_on')

        if task == depends_on:
            raise serializers.ValidationError("Task cannot depend on itself.")

        # Check for circular dependency (simplified check)
        # In production, do full graph traversal
        existing_deps = TaskDependency.objects.filter(task=depends_on)
        for dep in existing_deps:
            if dep.depends_on == task:
                raise serializers.ValidationError(
                    "Circular dependency detected."
                )

        return attrs


class TaskLogSerializer(serializers.ModelSerializer):
    """Serializer for TaskLog model."""

    task_title = serializers.CharField(source='task.title', read_only=True)
    agent_name = serializers.CharField(
        source='agent.agent_type.name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = TaskLog
        fields = [
            'id', 'task', 'task_title', 'agent', 'agent_name',
            'log_type', 'message', 'details', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TaskLogListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for task log lists."""

    agent_name = serializers.CharField(
        source='agent.agent_type.name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = TaskLog
        fields = ['id', 'log_type', 'message', 'agent_name', 'created_at']
        read_only_fields = fields


class TaskStatusUpdateSerializer(serializers.Serializer):
    """Serializer for task status updates."""

    status = serializers.ChoiceField(choices=TaskStatus.choices)
    notes = serializers.CharField(required=False, allow_blank=True)


class TaskDetailSerializer(TaskSerializer):
    """Detailed task serializer with dependencies and logs."""

    dependencies = serializers.SerializerMethodField()
    subtasks = serializers.SerializerMethodField()
    recent_logs = serializers.SerializerMethodField()

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + [
            'dependencies', 'subtasks', 'recent_logs'
        ]

    def get_dependencies(self, obj):
        """Get task dependencies."""
        deps = obj.dependencies.select_related('depends_on').all()
        return TaskDependencySerializer(deps, many=True).data

    def get_subtasks(self, obj):
        """Get subtasks."""
        subtasks = Task.objects.filter(parent_task=obj)
        return TaskListSerializer(subtasks, many=True).data

    def get_recent_logs(self, obj):
        """Get recent task logs."""
        logs = obj.tasklog_set.select_related('agent').order_by('-created_at')[:10]
        return TaskLogListSerializer(logs, many=True).data
