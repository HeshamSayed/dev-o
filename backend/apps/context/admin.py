"""
Admin for context app.
"""

from django.contrib import admin
from apps.context.models import Memory, Decision, EventLog


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'memory_type', 'project', 'importance', 'access_count', 'created_at']
    list_filter = ['memory_type', 'created_at']
    search_fields = ['title', 'content', 'project__name']
    readonly_fields = ['access_count', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(Decision)
class DecisionAdmin(admin.ModelAdmin):
    list_display = ['title', 'decision_type', 'project', 'status', 'made_by_agent', 'created_at']
    list_filter = ['decision_type', 'status', 'created_at']
    search_fields = ['title', 'description', 'project__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ['sequence_number', 'event_type', 'project', 'actor_type', 'actor_id', 'created_at']
    list_filter = ['event_type', 'actor_type', 'created_at']
    search_fields = ['project__name', 'event_type']
    readonly_fields = ['sequence_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
