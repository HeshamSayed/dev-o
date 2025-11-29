"""
Admin for agents app.
"""

from django.contrib import admin
from apps.agents.models import (
    AgentType,
    AgentInstance,
    AgentMessage,
    AgentAction
)


@admin.register(AgentType)
class AgentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'hierarchy_level', 'is_active']
    list_filter = ['hierarchy_level', 'is_active']
    search_fields = ['name', 'role']


@admin.register(AgentInstance)
class AgentInstanceAdmin(admin.ModelAdmin):
    list_display = ['agent_type', 'project', 'status', 'current_task', 'last_active_at']
    list_filter = ['status', 'agent_type', 'created_at']
    search_fields = ['project__name', 'agent_type__name']
    readonly_fields = ['created_at', 'updated_at', 'last_active_at']
    date_hierarchy = 'created_at'


@admin.register(AgentMessage)
class AgentMessageAdmin(admin.ModelAdmin):
    list_display = ['from_agent', 'to_agent', 'message_type', 'requires_response', 'responded', 'created_at']
    list_filter = ['message_type', 'requires_response', 'responded', 'created_at']
    search_fields = ['project__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(AgentAction)
class AgentActionAdmin(admin.ModelAdmin):
    list_display = ['agent', 'action_type', 'task', 'status', 'is_reversible', 'created_at']
    list_filter = ['action_type', 'status', 'is_reversible', 'created_at']
    search_fields = ['project__name', 'agent__agent_type__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
