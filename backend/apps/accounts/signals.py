"""
Signals for accounts app.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User, Subscription, SubscriptionTier


@receiver(post_save, sender=User)
def create_user_subscription(sender, instance, created, **kwargs):
    """
    Create a default subscription for new users.
    """
    if created:
        Subscription.objects.create(
            user=instance,
            tier=SubscriptionTier.FREE
        )
