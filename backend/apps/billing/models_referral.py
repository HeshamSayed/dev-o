"""
Referral system models for DEV-O.
"""

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class ReferralCode(models.Model):
    """Unique referral code for each user."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referral_code'
    )
    code = models.CharField(max_length=20, unique=True, db_index=True)

    # Stats
    clicks = models.IntegerField(default=0)
    signups = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)  # Upgrades to paid

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'billing_referral_code'

    def __str__(self):
        return f"{self.user.email} - {self.code}"


class Referral(models.Model):
    """Track individual referrals."""

    STATUS_CHOICES = [
        ('clicked', 'Clicked'),
        ('signed_up', 'Signed Up'),
        ('converted', 'Converted to Paid'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referrals_made'
    )
    referee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referred_by',
        null=True,
        blank=True
    )
    referral_code = models.ForeignKey(
        ReferralCode,
        on_delete=models.CASCADE,
        related_name='referrals'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='clicked')

    # Tracking
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    clicked_at = models.DateTimeField(auto_now_add=True)
    signed_up_at = models.DateTimeField(null=True, blank=True)
    converted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'billing_referral'
        indexes = [
            models.Index(fields=['referrer', 'status']),
            models.Index(fields=['referral_code']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        referee_email = self.referee.email if self.referee else 'Anonymous'
        return f"{self.referrer.email} → {referee_email} ({self.status})"


class ReferralReward(models.Model):
    """Rewards earned from referrals."""

    REWARD_TYPES = [
        ('extra_messages', 'Extra Messages'),
        ('extra_requests', 'Extra Project Requests'),
        ('account_credit', 'Account Credit'),
        ('feature_unlock', 'Feature Unlock'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('redeemed', 'Redeemed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='referral_rewards'
    )
    referral = models.ForeignKey(
        Referral,
        on_delete=models.CASCADE,
        related_name='rewards',
        null=True,
        blank=True
    )

    reward_type = models.CharField(max_length=20, choices=REWARD_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Reward details
    amount = models.IntegerField(default=0)  # e.g., 10 messages, $10 credit
    description = models.TextField()

    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    redeemed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'billing_referral_reward'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['valid_until']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.reward_type} ({self.amount})"

    def is_valid(self):
        """Check if reward is still valid."""
        now = timezone.now()
        return (
            self.status == 'active' and
            self.valid_from <= now <= self.valid_until
        )

    def activate(self):
        """Activate the reward."""
        self.status = 'active'
        self.save()

    def redeem(self):
        """Mark reward as redeemed."""
        self.status = 'redeemed'
        self.redeemed_at = timezone.now()
        self.save()

    def expire(self):
        """Mark reward as expired."""
        self.status = 'expired'
        self.save()
