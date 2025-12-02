"""
Serializers for billing and subscription data.
"""

from rest_framework import serializers
from .models import Plan, Subscription, UsageTracker, UsageLog


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for pricing plans."""

    class Meta:
        model = Plan
        fields = [
            'id',
            'name',
            'plan_type',
            'price_monthly',
            'price_yearly',
            # Chat limits
            'messages_per_window',
            'max_conversations',
            'context_window',
            # Project limits
            'max_active_projects',
            'max_archived_projects',
            'max_files_per_project',
            'project_requests_per_window',
            # Agent limits
            'available_agents',
            'max_concurrent_agents',
            # Storage limits
            'storage_limit_mb',
            'max_file_size_kb',
            'retention_days',
            # AI Model
            'model_tier',
            'max_output_tokens',
            # Rate limits
            'requests_per_minute',
            'max_concurrent_connections',
            'queue_priority',
            # Features
            'has_thinking_mode',
            'has_download',
            'has_git_integration',
            'has_api_access',
            'has_chat_search',
            'is_active',
        ]
        read_only_fields = ['id']


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for user subscriptions."""

    plan = PlanSerializer(read_only=True)
    plan_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Subscription
        fields = [
            'id',
            'user',
            'plan',
            'plan_id',
            'status',
            'billing_cycle',
            'stripe_subscription_id',
            'stripe_customer_id',
            'current_period_start',
            'current_period_end',
            'trial_end',
            'cancelled_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'stripe_subscription_id',
            'stripe_customer_id',
            'created_at',
            'updated_at',
        ]


class UsageTrackerSerializer(serializers.ModelSerializer):
    """Serializer for usage tracking."""

    class Meta:
        model = UsageTracker
        fields = [
            'id',
            'user',
            'window_start',
            'window_end',
            'chat_messages_used',
            'chat_tokens_used',
            'project_requests_used',
            'project_tokens_used',
            'storage_used_bytes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UsageLogSerializer(serializers.ModelSerializer):
    """Serializer for usage logs."""

    class Meta:
        model = UsageLog
        fields = [
            'id',
            'user',
            'usage_type',
            'conversation_id',
            'project_id',
            'input_tokens',
            'output_tokens',
            'estimated_cost',
            'model_used',
            'duration_ms',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']


class UsageSummarySerializer(serializers.Serializer):
    """Serializer for usage summary response."""

    plan = serializers.DictField()
    window = serializers.DictField()
    chat = serializers.DictField()
    projects = serializers.DictField()
    features = serializers.DictField()
