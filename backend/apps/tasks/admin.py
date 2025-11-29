"""
Admin for tasks app.
"""

from django.contrib import admin
from apps.tasks.models import Task, TaskDependency, TaskLog


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'task_type', 'status', 'priority', 'assigned_to', 'created_at']
    list_filter = ['task_type', 'status', 'priority', 'created_at']
    search_fields = ['title', 'description', 'project__name']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    date_hierarchy = 'created_at'


@admin.register(TaskDependency)
class TaskDependencyAdmin(admin.ModelAdmin):
    list_display = ['task', 'depends_on', 'dependency_type', 'created_at']
    list_filter = ['dependency_type', 'created_at']
    search_fields = ['task__title', 'depends_on__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    list_display = ['task', 'agent', 'log_type', 'created_at']
    list_filter = ['log_type', 'created_at']
    search_fields = ['task__title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
