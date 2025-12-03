"""Agent serializers."""

from rest_framework import serializers
from .models import Agent


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'name', 'type', 'system_prompt', 'capabilities', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
