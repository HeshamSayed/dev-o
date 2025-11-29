"""
Admin for projects app.
"""

from django.contrib import admin
from apps.projects.models import Project, ProjectCheckpoint


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description', 'owner__email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(ProjectCheckpoint)
class ProjectCheckpointAdmin(admin.ModelAdmin):
    list_display = ['project', 'name', 'created_by', 'is_auto', 'created_at']
    list_filter = ['is_auto', 'created_at']
    search_fields = ['project__name', 'name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
