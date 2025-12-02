"""
Django admin configuration for referral models.
"""

from django.contrib import admin
from apps.billing.models_referral import ReferralCode, Referral, ReferralReward


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    """Admin interface for referral codes."""

    list_display = ['code', 'user', 'clicks', 'signups', 'conversions', 'created_at']
    list_filter = ['created_at']
    search_fields = ['code', 'user__email', 'user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['user']

    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'user', 'code')
        }),
        ('Statistics', {
            'fields': ('clicks', 'signups', 'conversions')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    """Admin interface for referrals."""

    list_display = [
        'referral_code',
        'referrer',
        'referee',
        'status',
        'clicked_at',
        'signed_up_at',
    ]
    list_filter = ['status', 'clicked_at', 'signed_up_at']
    search_fields = [
        'referrer__email',
        'referee__email',
        'referral_code__code',
        'ip_address',
    ]
    readonly_fields = [
        'id',
        'clicked_at',
        'signed_up_at',
        'converted_at',
        'ip_address',
        'user_agent',
    ]
    raw_id_fields = ['referrer', 'referee', 'referral_code']
    date_hierarchy = 'clicked_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'referrer', 'referee', 'referral_code', 'status')
        }),
        ('Tracking', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Dates', {
            'fields': ('clicked_at', 'signed_up_at', 'converted_at')
        }),
    )


@admin.register(ReferralReward)
class ReferralRewardAdmin(admin.ModelAdmin):
    """Admin interface for referral rewards."""

    list_display = [
        'user',
        'reward_type',
        'amount',
        'status',
        'valid_from',
        'valid_until',
        'created_at',
    ]
    list_filter = ['reward_type', 'status', 'created_at']
    search_fields = ['user__email', 'user__username', 'description']
    readonly_fields = ['id', 'created_at', 'redeemed_at']
    raw_id_fields = ['user', 'referral']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'user', 'referral', 'reward_type', 'status')
        }),
        ('Reward Details', {
            'fields': ('amount', 'description')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Metadata', {
            'fields': ('created_at', 'redeemed_at')
        }),
    )

    actions = ['activate_rewards', 'expire_rewards']

    def activate_rewards(self, request, queryset):
        """Activate selected rewards."""
        count = queryset.filter(status='pending').update(status='active')
        self.message_user(request, f'{count} rewards activated.')
    activate_rewards.short_description = 'Activate selected rewards'

    def expire_rewards(self, request, queryset):
        """Expire selected rewards."""
        count = queryset.filter(status='active').update(status='expired')
        self.message_user(request, f'{count} rewards expired.')
    expire_rewards.short_description = 'Expire selected rewards'
