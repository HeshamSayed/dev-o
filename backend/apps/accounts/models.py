"""
User and Subscription Models

Design Decisions:
1. Extend Django's AbstractUser for custom fields
2. Subscription tracks tier and limits
3. Usage tracking for rate limiting
4. API key support for programmatic access
"""

import uuid
import secrets
import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from core.mixins import UUIDPrimaryKeyMixin, TimestampMixin


class User(AbstractUser, UUIDPrimaryKeyMixin, TimestampMixin):
    """Extended user model with subscription support"""

    email = models.EmailField(unique=True, db_index=True)

    # Profile
    company_name = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')

    # Settings
    preferred_llm = models.CharField(
        max_length=50,
        default='deepseek-r1:7b',
        choices=[
            ('deepseek-r1:7b', 'DeepSeek R1 7B (Local)'),
            ('deepseek-r1:14b', 'DeepSeek R1 14B (Local)'),
            ('gpt-4', 'GPT-4 (API)'),
            ('claude-3-opus', 'Claude 3 Opus (API)'),
        ]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @property
    def subscription_tier(self):
        """Get user's subscription tier."""
        try:
            return self.subscription.tier
        except Subscription.DoesNotExist:
            return SubscriptionTier.FREE


class SubscriptionTier(models.TextChoices):
    """Subscription tier choices."""
    FREE = 'free', 'Free'
    PRO = 'pro', 'Pro'
    TEAM = 'team', 'Team'
    ENTERPRISE = 'enterprise', 'Enterprise'


class Subscription(UUIDPrimaryKeyMixin, TimestampMixin):
    """User subscription and limits"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    tier = models.CharField(
        max_length=20,
        choices=SubscriptionTier.choices,
        default=SubscriptionTier.FREE,
        db_index=True
    )

    # Limits based on tier
    max_projects = models.IntegerField(default=1)
    max_agents_per_project = models.IntegerField(default=2)
    max_actions_per_day = models.IntegerField(default=100)
    can_use_api_llms = models.BooleanField(default=False)
    can_use_custom_agents = models.BooleanField(default=False)

    # Billing
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)

    # Status
    is_active = models.BooleanField(default=True, db_index=True)
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f"{self.user.email} - {self.tier}"

    def get_limits(self):
        """Return tier-specific limits"""
        tier_limits = {
            SubscriptionTier.FREE: {
                'max_projects': 1,
                'max_agents_per_project': 2,
                'max_actions_per_day': 100,
                'can_use_api_llms': False,
            },
            SubscriptionTier.PRO: {
                'max_projects': 5,
                'max_agents_per_project': 10,
                'max_actions_per_day': 1000,
                'can_use_api_llms': True,
            },
            SubscriptionTier.TEAM: {
                'max_projects': -1,  # unlimited
                'max_agents_per_project': -1,
                'max_actions_per_day': -1,
                'can_use_api_llms': True,
            },
        }
        return tier_limits.get(self.tier, tier_limits[SubscriptionTier.FREE])

    def update_limits(self):
        """Update subscription limits based on tier."""
        limits = self.get_limits()
        self.max_projects = limits['max_projects']
        self.max_agents_per_project = limits['max_agents_per_project']
        self.max_actions_per_day = limits['max_actions_per_day']
        self.can_use_api_llms = limits['can_use_api_llms']
        self.save(update_fields=[
            'max_projects',
            'max_agents_per_project',
            'max_actions_per_day',
            'can_use_api_llms'
        ])


class UsageTracking(UUIDPrimaryKeyMixin):
    """Track daily usage for rate limiting"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='usage_records'
    )

    date = models.DateField(default=timezone.now, db_index=True)
    agent_actions = models.IntegerField(default=0)
    llm_tokens_used = models.IntegerField(default=0)
    files_generated = models.IntegerField(default=0)

    class Meta:
        db_table = 'usage_tracking'
        unique_together = ['user', 'date']
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
        verbose_name = 'Usage Tracking'
        verbose_name_plural = 'Usage Tracking'

    def __str__(self):
        return f"{self.user.email} - {self.date}"

    @classmethod
    def get_or_create_today(cls, user):
        """Get or create usage record for today."""
        today = timezone.now().date()
        usage, created = cls.objects.get_or_create(
            user=user,
            date=today
        )
        return usage

    def increment_actions(self, count=1):
        """Increment agent actions count."""
        self.agent_actions += count
        self.save(update_fields=['agent_actions'])

    def increment_tokens(self, count):
        """Increment LLM tokens used."""
        self.llm_tokens_used += count
        self.save(update_fields=['llm_tokens_used'])

    def increment_files(self, count=1):
        """Increment files generated count."""
        self.files_generated += count
        self.save(update_fields=['files_generated'])


class APIKey(UUIDPrimaryKeyMixin, TimestampMixin):
    """API keys for programmatic access"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='api_keys'
    )

    name = models.CharField(max_length=100)
    key_hash = models.CharField(max_length=64, unique=True, db_index=True)
    key_prefix = models.CharField(max_length=8)  # First 8 chars for identification

    # Permissions
    scopes = models.JSONField(default=list)  # ['read', 'write', 'admin']

    # Status
    is_active = models.BooleanField(default=True, db_index=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'api_keys'
        ordering = ['-created_at']
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'

    def __str__(self):
        return f"{self.name} ({self.key_prefix}...)"

    @classmethod
    def generate_key(cls):
        """Generate a new API key"""
        key = f"devo_{secrets.token_urlsafe(32)}"
        return key

    @classmethod
    def hash_key(cls, key):
        """Hash a key for storage"""
        return hashlib.sha256(key.encode()).hexdigest()

    @classmethod
    def create_key(cls, user, name, scopes=None):
        """Create a new API key for a user."""
        key = cls.generate_key()
        key_hash = cls.hash_key(key)
        key_prefix = key[:12]  # devo_ + first 8 chars

        api_key = cls.objects.create(
            user=user,
            name=name,
            key_hash=key_hash,
            key_prefix=key_prefix,
            scopes=scopes or ['read', 'write']
        )

        # Return both the API key object and the plain key (only time we have it)
        return api_key, key

    def verify_key(self, key):
        """Verify a key against this API key."""
        return self.key_hash == self.hash_key(key)

    def mark_used(self):
        """Mark this API key as used."""
        self.last_used_at = timezone.now()
        self.save(update_fields=['last_used_at'])

    def is_valid(self):
        """Check if API key is valid (active and not expired)."""
        if not self.is_active:
            return False

        if self.expires_at and self.expires_at < timezone.now():
            return False

        return True
