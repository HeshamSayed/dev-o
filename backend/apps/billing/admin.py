"""
Django admin configuration for billing models.
"""

from django.contrib import admin
from .models import Plan, Subscription, UsageTracker, UsageLog

# Import referral admin registrations
from . import admin_referral  # noqa: F401


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Admin interface for pricing plans."""

    list_display = [
        'name',
        'plan_type',
        'price_monthly',
        'price_yearly',
        'messages_per_window',
        'project_requests_per_window',
        'is_active',
    ]
    list_filter = ['plan_type', 'is_active']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at']

    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'name', 'plan_type', 'price_monthly', 'price_yearly', 'is_active')
        }),
        ('Chat Limits (per 2-hour window)', {
            'fields': ('messages_per_window', 'max_conversations', 'context_window')
        }),
        ('Project Limits (per 2-hour window)', {
            'fields': (
                'max_active_projects',
                'max_archived_projects',
                'max_files_per_project',
                'project_requests_per_window'
            )
        }),
        ('Agent Limits', {
            'fields': ('available_agents', 'max_concurrent_agents')
        }),
        ('Storage Limits', {
            'fields': ('storage_limit_mb', 'max_file_size_kb', 'retention_days')
        }),
        ('AI Model', {
            'fields': ('model_tier', 'max_output_tokens')
        }),
        ('Rate Limits', {
            'fields': ('requests_per_minute', 'max_concurrent_connections', 'queue_priority')
        }),
        ('Features', {
            'fields': (
                'has_thinking_mode',
                'has_download',
                'has_git_integration',
                'has_api_access',
                'has_chat_search'
            )
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin interface for user subscriptions."""

    list_display = [
        'user',
        'plan',
        'status',
        'billing_cycle',
        'current_period_start',
        'current_period_end',
    ]
    list_filter = ['status', 'billing_cycle', 'plan']
    search_fields = ['user__email', 'user__username', 'stripe_customer_id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['user']

    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'user', 'plan', 'status', 'billing_cycle')
        }),
        ('Stripe Info', {
            'fields': ('stripe_subscription_id', 'stripe_customer_id')
        }),
        ('Dates', {
            'fields': (
                'current_period_start',
                'current_period_end',
                'trial_end',
                'cancelled_at'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(UsageTracker)
class UsageTrackerAdmin(admin.ModelAdmin):
    """Admin interface for usage tracking."""

    list_display = [
        'user',
        'window_start',
        'window_end',
        'chat_messages_used',
        'project_requests_used',
    ]
    list_filter = ['window_start']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['user']
    date_hierarchy = 'window_start'

    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'user', 'window_start', 'window_end')
        }),
        ('Chat Usage', {
            'fields': ('chat_messages_used', 'chat_tokens_used')
        }),
        ('Project Usage', {
            'fields': ('project_requests_used', 'project_tokens_used')
        }),
        ('Storage Usage', {
            'fields': ('storage_used_bytes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(UsageLog)
class UsageLogAdmin(admin.ModelAdmin):
    """Admin interface for usage logs."""

    list_display = [
        'user',
        'usage_type',
        'model_used',
        'input_tokens',
        'output_tokens',
        'duration_ms',
        'created_at',
    ]
    list_filter = ['usage_type', 'model_used', 'created_at']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['id', 'created_at']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'user', 'usage_type')
        }),
        ('Related Objects', {
            'fields': ('conversation_id', 'project_id')
        }),
        ('Token Usage', {
            'fields': ('input_tokens', 'output_tokens', 'estimated_cost')
        }),
        ('Metadata', {
            'fields': ('model_used', 'duration_ms', 'created_at')
        }),
    )
