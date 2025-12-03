"""
Serializers for referral system.
"""

from rest_framework import serializers
from apps.billing.models_referral import ReferralCode, Referral, ReferralReward


class ReferralCodeSerializer(serializers.ModelSerializer):
    """Serializer for referral codes."""

    referral_link = serializers.SerializerMethodField()

    class Meta:
        model = ReferralCode
        fields = [
            'id',
            'code',
            'referral_link',
            'clicks',
            'signups',
            'conversions',
            'created_at',
        ]
        read_only_fields = ['id', 'code', 'clicks', 'signups', 'conversions', 'created_at']

    def get_referral_link(self, obj):
        """Generate full referral link."""
        request = self.context.get('request')
        if request:
            # Get frontend URL from settings or request
            from django.conf import settings
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
            return f"{frontend_url}/signup?ref={obj.code}"
        return f"/signup?ref={obj.code}"


class ReferralSerializer(serializers.ModelSerializer):
    """Serializer for referrals."""

    referrer_email = serializers.EmailField(source='referrer.email', read_only=True)
    referee_email = serializers.EmailField(source='referee.email', read_only=True, allow_null=True)
    referral_code_display = serializers.CharField(source='referral_code.code', read_only=True)

    class Meta:
        model = Referral
        fields = [
            'id',
            'referrer_email',
            'referee_email',
            'referral_code_display',
            'status',
            'clicked_at',
            'signed_up_at',
            'converted_at',
        ]
        read_only_fields = ['id']


class ReferralRewardSerializer(serializers.ModelSerializer):
    """Serializer for referral rewards."""

    is_valid = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = ReferralReward
        fields = [
            'id',
            'reward_type',
            'status',
            'amount',
            'description',
            'valid_from',
            'valid_until',
            'is_valid',
            'days_remaining',
            'created_at',
            'redeemed_at',
        ]
        read_only_fields = ['id', 'created_at', 'redeemed_at']

    def get_is_valid(self, obj):
        """Check if reward is currently valid."""
        return obj.is_valid()

    def get_days_remaining(self, obj):
        """Get days remaining until expiry."""
        from django.utils import timezone
        if obj.status != 'active':
            return 0

        now = timezone.now()
        if now > obj.valid_until:
            return 0

        delta = obj.valid_until - now
        return delta.days


class TrackReferralSerializer(serializers.Serializer):
    """Serializer for tracking referral clicks."""

    code = serializers.CharField(max_length=20, required=True)
