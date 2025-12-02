"""
Billing models for DEV-O pricing system.
2-hour reset windows for better engagement!
"""

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Plan(models.Model):
    """Subscription plan definitions."""

    PLAN_TYPES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('team', 'Team'),
        ('enterprise', 'Enterprise'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2)

    # Chat limits (per 2-hour window)
    messages_per_window = models.IntegerField(default=10)
    max_conversations = models.IntegerField(default=5)  # -1 for unlimited
    context_window = models.IntegerField(default=4096)

    # Project limits (per 2-hour window)
    max_active_projects = models.IntegerField(default=1)
    max_archived_projects = models.IntegerField(default=0)
    max_files_per_project = models.IntegerField(default=10)
    project_requests_per_window = models.IntegerField(default=2)

    # Agent limits
    available_agents = models.JSONField(default=list)
    max_concurrent_agents = models.IntegerField(default=1)

    # Storage limits
    storage_limit_mb = models.IntegerField(default=10)
    max_file_size_kb = models.IntegerField(default=100)
    retention_days = models.IntegerField(default=7)

    # AI Model
    model_tier = models.CharField(max_length=20, default='basic')
    max_output_tokens = models.IntegerField(default=1024)

    # Rate limits
    requests_per_minute = models.IntegerField(default=2)
    max_concurrent_connections = models.IntegerField(default=1)
    queue_priority = models.IntegerField(default=0)

    # Features
    has_thinking_mode = models.BooleanField(default=False)
    has_download = models.BooleanField(default=False)
    has_git_integration = models.BooleanField(default=False)
    has_api_access = models.BooleanField(default=False)
    has_chat_search = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'billing_plan'

    def __str__(self):
        return f"{self.name} (${self.price_monthly}/mo)"


class Subscription(models.Model):
    """User subscription."""

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('past_due', 'Past Due'),
        ('trialing', 'Trialing'),
    ]

    BILLING_CYCLE = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription'
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE, default='monthly')

    # Payment info (Stripe)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    # Dates
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    trial_end = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'billing_subscription'

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

    @property
    def is_active(self):
        return self.status in ['active', 'trialing']


class UsageTracker(models.Model):
    """Track usage per 2-hour window."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='usage_records'
    )
    window_start = models.DateTimeField()  # Start of 2-hour window
    window_end = models.DateTimeField()    # End of 2-hour window

    # Chat usage
    chat_messages_used = models.IntegerField(default=0)
    chat_tokens_used = models.IntegerField(default=0)

    # Project usage
    project_requests_used = models.IntegerField(default=0)
    project_tokens_used = models.IntegerField(default=0)

    # Storage usage (cumulative)
    storage_used_bytes = models.BigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'billing_usage_tracker'
        unique_together = ['user', 'window_start']
        indexes = [
            models.Index(fields=['user', 'window_start']),
            models.Index(fields=['window_end']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.window_start}"


class UsageLog(models.Model):
    """Detailed log of each usage event."""

    USAGE_TYPES = [
        ('chat_message', 'Chat Message'),
        ('project_request', 'Project Request'),
        ('file_created', 'File Created'),
        ('file_updated', 'File Updated'),
        ('download', 'Project Download'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='usage_logs'
    )
    usage_type = models.CharField(max_length=30, choices=USAGE_TYPES)

    # Related objects
    conversation_id = models.UUIDField(null=True, blank=True)
    project_id = models.UUIDField(null=True, blank=True)

    # Token usage
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)

    # Cost tracking
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=6, default=0)

    # Metadata
    model_used = models.CharField(max_length=100, blank=True)
    duration_ms = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'billing_usage_log'
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['usage_type', 'created_at']),
        ]


# Import referral models to make them available
from .models_referral import ReferralCode, Referral, ReferralReward  # noqa: F401, E402

__all__ = [
    'Plan',
    'Subscription',
    'UsageTracker',
    'UsageLog',
    'ReferralCode',
    'Referral',
    'ReferralReward',
]
