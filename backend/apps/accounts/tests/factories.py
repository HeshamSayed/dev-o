"""
Factories for accounts app models.
"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.accounts.models import User, Subscription, UsageTracking, APIKey

fake = Faker()


class UserFactory(DjangoModelFactory):
    """Factory for User model."""

    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    username = factory.Sequence(lambda n: f'user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    is_active = True
    is_staff = False
    is_superuser = False


class SubscriptionFactory(DjangoModelFactory):
    """Factory for Subscription model."""

    class Meta:
        model = Subscription

    user = factory.SubFactory(UserFactory)
    tier = 'free'
    max_projects = 3
    max_agents_per_project = 5
    max_actions_per_day = 100
    can_use_api_llms = False
    is_active = True


class UsageTrackingFactory(DjangoModelFactory):
    """Factory for UsageTracking model."""

    class Meta:
        model = UsageTracking

    user = factory.SubFactory(UserFactory)
    date = factory.Faker('date_this_month')
    agent_actions = factory.Faker('random_int', min=0, max=100)
    llm_tokens_used = factory.Faker('random_int', min=0, max=10000)
    files_generated = factory.Faker('random_int', min=0, max=50)


class APIKeyFactory(DjangoModelFactory):
    """Factory for APIKey model."""

    class Meta:
        model = APIKey

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'API Key {n}')
    key_hash = factory.Faker('sha256')
    key_prefix = factory.Sequence(lambda n: f'devo_{n:04d}')
    is_active = True
