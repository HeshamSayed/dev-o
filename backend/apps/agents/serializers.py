"""Agent serializers."""

from rest_framework import serializers
from .models import Agent, AgentAssignment


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'name', 'type', 'system_prompt', 'capabilities', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class AgentAssignmentSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    agent_type = serializers.CharField(source='agent.type', read_only=True)

    class Meta:
        model = AgentAssignment
        fields = ['id', 'agent', 'agent_name', 'agent_type', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
