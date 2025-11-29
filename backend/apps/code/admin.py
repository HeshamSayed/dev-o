"""
Admin for code app.
"""

from django.contrib import admin
from apps.code.models import CodeArtifact, CodeChange, ArtifactRegistry


@admin.register(CodeArtifact)
class CodeArtifactAdmin(admin.ModelAdmin):
    list_display = ['file_path', 'project', 'language', 'line_count', 'last_modified_by', 'updated_at']
    list_filter = ['language', 'created_at']
    search_fields = ['file_path', 'file_name', 'project__name']
    readonly_fields = ['content_hash', 'line_count', 'file_name', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(CodeChange)
class CodeChangeAdmin(admin.ModelAdmin):
    list_display = ['artifact', 'change_type', 'agent', 'task', 'created_at']
    list_filter = ['change_type', 'created_at']
    search_fields = ['artifact__file_path', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(ArtifactRegistry)
class ArtifactRegistryAdmin(admin.ModelAdmin):
    list_display = ['name', 'artifact_type', 'project', 'file_path', 'is_active', 'created_at']
    list_filter = ['artifact_type', 'is_active', 'created_at']
    search_fields = ['name', 'file_path', 'project__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
