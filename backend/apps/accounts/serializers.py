"""
Account Serializers

Serializers for user accounts, subscriptions, and API keys.
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User, Subscription, UsageTracking, APIKey


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm', 'preferred_llm',
            'company_name', 'timezone',
            'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined', 'is_active']

    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            preferred_llm=validated_data.get('preferred_llm', 'deepseek-r1:7b'),
            company_name=validated_data.get('company_name', ''),
            timezone=validated_data.get('timezone', 'UTC')
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile (excludes sensitive data)."""

    subscription = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'preferred_llm', 'company_name', 'timezone',
            'date_joined', 'subscription'
        ]
        read_only_fields = ['id', 'username', 'email', 'date_joined']

    def get_subscription(self, obj):
        """Get user's subscription info."""
        try:
            subscription = obj.subscription
            return {
                'tier': subscription.tier,
                'max_projects': subscription.max_projects,
                'max_agents_per_project': subscription.max_agents_per_project,
                'is_active': subscription.is_active
            }
        except Subscription.DoesNotExist:
            return None


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscription model."""

    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Subscription
        fields = [
            'id', 'user', 'user_email', 'tier', 'max_projects',
            'max_agents_per_project', 'max_llm_calls_per_month',
            'max_tokens_per_call', 'is_active', 'start_date', 'end_date',
            'auto_renew', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UsageTrackingSerializer(serializers.ModelSerializer):
    """Serializer for UsageTracking model."""

    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UsageTracking
        fields = [
            'id', 'user', 'user_email', 'date', 'llm_calls',
            'tokens_used', 'agents_created', 'tasks_completed',
            'files_created', 'api_calls', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class APIKeySerializer(serializers.ModelSerializer):
    """Serializer for APIKey model."""

    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = APIKey
        fields = [
            'id', 'user', 'user_email', 'name', 'key_prefix',
            'is_active', 'created_at', 'last_used_at', 'expires_at'
        ]
        read_only_fields = ['id', 'user', 'key_prefix', 'created_at', 'last_used_at']

    def to_representation(self, instance):
        """Never expose the full API key."""
        representation = super().to_representation(instance)
        # Only show key prefix, never the full key
        return representation


class APIKeyCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating API keys (returns full key once)."""

    full_key = serializers.CharField(read_only=True)

    class Meta:
        model = APIKey
        fields = ['id', 'name', 'expires_at', 'full_key']
        read_only_fields = ['id', 'full_key']

    def create(self, validated_data):
        """Create API key and return full key."""
        api_key = APIKey.objects.create(
            user=self.context['request'].user,
            name=validated_data['name'],
            expires_at=validated_data.get('expires_at')
        )
        # Generate full key
        import secrets
        full_key = f"devo_{secrets.token_urlsafe(32)}"
        api_key.set_key(full_key)

        # Attach full key to instance for serialization
        api_key.full_key = full_key
        return api_key
