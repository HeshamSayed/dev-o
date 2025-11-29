"""
Unit tests for accounts models.
"""
import pytest
from django.contrib.auth import get_user_model
from apps.accounts.models import Subscription, UsageTracking, APIKey
from apps.accounts.tests.factories import (
    UserFactory,
    SubscriptionFactory,
    UsageTrackingFactory,
    APIKeyFactory
)

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Tests for User model."""

    def test_create_user(self):
        """Test creating a user."""
        user = UserFactory(email='test@example.com', username='testuser')

        assert user.email == 'test@example.com'
        assert user.username == 'testuser'
        assert user.is_active is True
        assert user.check_password('testpass123')

    def test_user_str(self):
        """Test user string representation."""
        user = UserFactory(email='test@example.com')
        assert str(user) == 'test@example.com'

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = UserFactory(is_staff=True, is_superuser=True)

        assert user.is_staff is True
        assert user.is_superuser is True


@pytest.mark.django_db
class TestSubscriptionModel:
    """Tests for Subscription model."""

    def test_create_subscription(self):
        """Test creating a subscription."""
        user = UserFactory()
        subscription = SubscriptionFactory(user=user, tier='pro')

        assert subscription.user == user
        assert subscription.tier == 'pro'
        assert subscription.is_active is True

    def test_subscription_str(self):
        """Test subscription string representation."""
        user = UserFactory(email='test@example.com')
        subscription = SubscriptionFactory(user=user, tier='pro')

        assert str(subscription) == 'test@example.com - pro'

    def test_free_tier_limits(self):
        """Test free tier subscription limits."""
        subscription = SubscriptionFactory(tier='free')

        assert subscription.max_projects == 3
        assert subscription.max_agents_per_project == 5
        assert subscription.can_use_api_llms is False


@pytest.mark.django_db
class TestUsageTrackingModel:
    """Tests for UsageTracking model."""

    def test_create_usage_tracking(self):
        """Test creating usage tracking record."""
        user = UserFactory()
        usage = UsageTrackingFactory(
            user=user,
            agent_actions=50,
            llm_tokens_used=1000
        )

        assert usage.user == user
        assert usage.agent_actions == 50
        assert usage.llm_tokens_used == 1000

    def test_unique_user_date(self):
        """Test that user and date combination is unique."""
        from datetime import date
        user = UserFactory()
        today = date.today()

        UsageTrackingFactory(user=user, date=today)

        # Should raise IntegrityError when trying to create duplicate
        with pytest.raises(Exception):
            UsageTrackingFactory(user=user, date=today)


@pytest.mark.django_db
class TestAPIKeyModel:
    """Tests for APIKey model."""

    def test_create_api_key(self):
        """Test creating an API key."""
        user = UserFactory()
        api_key = APIKeyFactory(user=user, name='Test Key')

        assert api_key.user == user
        assert api_key.name == 'Test Key'
        assert api_key.is_active is True

    def test_api_key_str(self):
        """Test API key string representation."""
        user = UserFactory(username='testuser')
        api_key = APIKeyFactory(user=user, name='Test Key')

        assert 'Test Key' in str(api_key)
        assert 'testuser' in str(api_key)
