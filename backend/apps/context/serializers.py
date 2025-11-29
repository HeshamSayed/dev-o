"""
Context Serializers

Serializers for memories, decisions, and event logs.
"""

from rest_framework import serializers
from .models import Memory, Decision, EventLog


class MemorySerializer(serializers.ModelSerializer):
    """Serializer for Memory model."""

    project_name = serializers.CharField(source='project.name', read_only=True)
    created_by_name = serializers.CharField(
        source='created_by_agent.agent_type.name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Memory
        fields = [
            'id', 'project', 'project_name', 'memory_type', 'title',
            'content', 'metadata', 'importance', 'embedding',
            'created_by_agent', 'created_by_name', 'access_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'embedding', 'access_count', 'created_at', 'updated_at'
        ]


class MemoryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for memory lists."""

    class Meta:
        model = Memory
        fields = [
            'id', 'memory_type', 'title', 'importance',
            'access_count', 'created_at'
        ]
        read_only_fields = fields


class MemoryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating memories."""

    class Meta:
        model = Memory
        fields = [
            'memory_type', 'title', 'content', 'metadata', 'importance'
        ]

    def create(self, validated_data):
        """Create memory."""
        memory = Memory.objects.create(
            project=self.context['project'],
            created_by_agent=self.context.get('created_by_agent'),
            **validated_data
        )

        return memory


class DecisionSerializer(serializers.ModelSerializer):
    """Serializer for Decision model."""

    project_name = serializers.CharField(source='project.name', read_only=True)
    made_by_name = serializers.CharField(
        source='made_by_agent.agent_type.name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Decision
        fields = [
            'id', 'project', 'project_name', 'decision_type', 'title',
            'description', 'reasoning', 'alternatives_considered',
            'affected_components', 'trade_offs', 'status',
            'made_by_agent', 'made_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DecisionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for decision lists."""

    made_by_name = serializers.CharField(
        source='made_by_agent.agent_type.name',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Decision
        fields = [
            'id', 'decision_type', 'title', 'status',
            'made_by_name', 'created_at'
        ]
        read_only_fields = fields


class DecisionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating decisions."""

    class Meta:
        model = Decision
        fields = [
            'decision_type', 'title', 'description', 'reasoning',
            'alternatives_considered', 'affected_components', 'trade_offs'
        ]

    def create(self, validated_data):
        """Create decision."""
        decision = Decision.objects.create(
            project=self.context['project'],
            made_by_agent=self.context.get('made_by_agent'),
            status='proposed',
            **validated_data
        )

        # Log decision event
        from apps.context.services.event_store import EventStore
        EventStore.log_decision_made(
            project=decision.project,
            decision_id=str(decision.id),
            decision_title=decision.title,
            made_by=str(self.context.get('made_by_agent').id) if self.context.get('made_by_agent') else 'user'
        )

        return decision


class DecisionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating decisions."""

    class Meta:
        model = Decision
        fields = [
            'description', 'reasoning', 'alternatives_considered',
            'affected_components', 'trade_offs', 'status'
        ]


class EventLogSerializer(serializers.ModelSerializer):
    """Serializer for EventLog model."""

    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = EventLog
        fields = [
            'id', 'project', 'project_name', 'sequence_number',
            'event_type', 'event_data', 'actor_type', 'actor_id',
            'created_at'
        ]
        read_only_fields = ['id', 'sequence_number', 'created_at']


class EventLogListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for event log lists."""

    class Meta:
        model = EventLog
        fields = [
            'id', 'sequence_number', 'event_type', 'actor_type',
            'actor_id', 'created_at'
        ]
        read_only_fields = fields


class EventLogDetailSerializer(EventLogSerializer):
    """Detailed event log serializer."""

    actor_details = serializers.SerializerMethodField()

    class Meta(EventLogSerializer.Meta):
        fields = EventLogSerializer.Meta.fields + ['actor_details']

    def get_actor_details(self, obj):
        """Get actor details based on actor type."""
        if obj.actor_type == 'agent':
            try:
                from apps.agents.models import AgentInstance
                agent = AgentInstance.objects.get(id=obj.actor_id)
                return {
                    'type': 'agent',
                    'name': agent.agent_type.name,
                    'role': agent.agent_type.role
                }
            except AgentInstance.DoesNotExist:
                return None

        elif obj.actor_type == 'user':
            try:
                from apps.accounts.models import User
                user = User.objects.get(id=obj.actor_id)
                return {
                    'type': 'user',
                    'username': user.username,
                    'email': user.email
                }
            except User.DoesNotExist:
                return None

        return {'type': obj.actor_type}


class ProjectTimelineSerializer(serializers.Serializer):
    """Serializer for project timeline."""

    sequence = serializers.IntegerField()
    type = serializers.CharField()
    actor = serializers.CharField()
    timestamp = serializers.DateTimeField()
    data = serializers.DictField()
