"""
Agent Serializers

Serializers for agent types, instances, messages, and actions.
"""

from rest_framework import serializers
from .models import AgentType, AgentInstance, AgentMessage, AgentAction, AgentStatus


class AgentTypeSerializer(serializers.ModelSerializer):
    """Serializer for AgentType model."""

    class Meta:
        model = AgentType
        fields = [
            'id', 'name', 'role', 'description', 'system_prompt',
            'available_tools', 'can_hire', 'hierarchy_level',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AgentTypeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for agent type lists."""

    class Meta:
        model = AgentType
        fields = ['id', 'name', 'role', 'description', 'hierarchy_level']
        read_only_fields = fields


class AgentInstanceSerializer(serializers.ModelSerializer):
    """Serializer for AgentInstance model."""

    agent_type_name = serializers.CharField(source='agent_type.name', read_only=True)
    agent_type_role = serializers.CharField(source='agent_type.role', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    hired_by_name = serializers.CharField(
        source='hired_by.agent_type.name',
        read_only=True,
        allow_null=True
    )
    current_task_title = serializers.CharField(
        source='current_task.title',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = AgentInstance
        fields = [
            'id', 'project', 'project_name', 'agent_type', 'agent_type_name',
            'agent_type_role', 'status', 'status_message', 'model',
            'temperature', 'hired_by', 'hired_by_name', 'current_task',
            'current_task_title', 'tasks_completed', 'working_memory',
            'conversation_history', 'last_active_at', 'created_at'
        ]
        read_only_fields = [
            'id', 'tasks_completed', 'last_active_at', 'created_at'
        ]


class AgentInstanceListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for agent instance lists."""

    agent_type_name = serializers.CharField(source='agent_type.name', read_only=True)
    current_task_title = serializers.CharField(
        source='current_task.title',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = AgentInstance
        fields = [
            'id', 'agent_type_name', 'status', 'current_task_title',
            'tasks_completed', 'last_active_at'
        ]
        read_only_fields = fields


class AgentHireSerializer(serializers.Serializer):
    """Serializer for hiring agents."""

    agent_type_role = serializers.CharField(
        help_text="Role of agent to hire (e.g., 'architect', 'backend_lead')"
    )
    initial_task = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional initial task description"
    )
    model = serializers.CharField(
        required=False,
        default='deepseek-r1:7b',
        help_text="LLM model to use"
    )
    temperature = serializers.FloatField(
        required=False,
        default=0.7,
        min_value=0.0,
        max_value=2.0
    )

    def validate_agent_type_role(self, value):
        """Validate agent type exists."""
        if not AgentType.objects.filter(role=value, is_active=True).exists():
            raise serializers.ValidationError(
                f"Agent type '{value}' not found or inactive."
            )
        return value

    def create(self, validated_data):
        """Create agent instance."""
        project = self.context['project']
        hiring_agent = self.context.get('hiring_agent')

        agent_type = AgentType.objects.get(role=validated_data['agent_type_role'])

        # Check hiring authority
        if hiring_agent:
            can_hire = hiring_agent.agent_type.can_hire or []
            if agent_type.role not in can_hire:
                raise serializers.ValidationError(
                    f"{hiring_agent.agent_type.name} cannot hire {agent_type.name}"
                )

        # Check subscription limits
        current_count = AgentInstance.objects.filter(project=project).count()
        max_agents = project.created_by.subscription.max_agents_per_project

        if current_count >= max_agents:
            raise serializers.ValidationError(
                f"Maximum agent limit reached ({max_agents}). Upgrade subscription."
            )

        # Create agent
        agent = AgentInstance.objects.create(
            project=project,
            agent_type=agent_type,
            hired_by=hiring_agent,
            model=validated_data.get('model', 'deepseek-r1:7b'),
            temperature=validated_data.get('temperature', 0.7),
            status=AgentStatus.IDLE
        )

        # Create initial task if provided
        initial_task_desc = validated_data.get('initial_task')
        if initial_task_desc:
            from apps.tasks.models import Task
            task = Task.objects.create(
                project=project,
                title=f"Initial task for {agent_type.name}",
                description=initial_task_desc,
                task_type='feature',
                priority='medium',
                created_by_agent=hiring_agent,
                assigned_to_agent=agent
            )

        # Log event
        from apps.context.services.event_store import EventStore
        EventStore.log_agent_hired(
            project=project,
            agent_type=agent_type.role,
            agent_id=str(agent.id),
            hired_by=str(hiring_agent.id) if hiring_agent else 'user'
        )

        return agent


class AgentMessageSerializer(serializers.ModelSerializer):
    """Serializer for AgentMessage model."""

    from_agent_name = serializers.CharField(
        source='from_agent.agent_type.name',
        read_only=True
    )
    to_agent_name = serializers.CharField(
        source='to_agent.agent_type.name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = AgentMessage
        fields = [
            'id', 'project', 'from_agent', 'from_agent_name',
            'to_agent', 'to_agent_name', 'message_type', 'content',
            'metadata', 'requires_response', 'response', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AgentMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating agent messages."""

    class Meta:
        model = AgentMessage
        fields = [
            'to_agent', 'message_type', 'content',
            'requires_response', 'metadata'
        ]

    def create(self, validated_data):
        """Create message."""
        message = AgentMessage.objects.create(
            project=self.context['project'],
            from_agent=self.context['from_agent'],
            **validated_data
        )
        return message


class AgentActionSerializer(serializers.ModelSerializer):
    """Serializer for AgentAction model."""

    agent_name = serializers.CharField(
        source='agent.agent_type.name',
        read_only=True
    )
    task_title = serializers.CharField(
        source='task.title',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = AgentAction
        fields = [
            'id', 'project', 'agent', 'agent_name', 'task', 'task_title',
            'action_type', 'action_data', 'is_reversible', 'reverse_action',
            'is_reversed', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AgentActionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for action lists."""

    agent_name = serializers.CharField(source='agent.agent_type.name', read_only=True)

    class Meta:
        model = AgentAction
        fields = [
            'id', 'agent_name', 'action_type', 'is_reversible',
            'is_reversed', 'created_at'
        ]
        read_only_fields = fields


class AgentStatusSerializer(serializers.Serializer):
    """Serializer for agent status updates."""

    status = serializers.ChoiceField(choices=AgentStatus.choices)
    status_message = serializers.CharField(required=False, allow_blank=True)


class AgentConversationSerializer(serializers.Serializer):
    """Serializer for agent conversation."""

    role = serializers.CharField()
    content = serializers.CharField()
    timestamp = serializers.DateTimeField()
    from_agent = serializers.CharField(required=False)
