"""
Signals for billing and referral system.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from apps.billing.models import Subscription
from services.referral_service import ReferralService

User = get_user_model()


@receiver(post_save, sender=User)
def create_referral_code(sender, instance, created, **kwargs):
    """
    Create referral code when user signs up.

    Args:
        sender: User model
        instance: User instance
        created: Whether this is a new user
    """
    if created:
        # Create referral code for new user
        try:
            ReferralService.create_referral_code(instance)
        except Exception as e:
            # Log error but don't fail user creation
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create referral code for {instance.email}: {str(e)}")


@receiver(post_save, sender=Subscription)
def handle_subscription_conversion(sender, instance, created, **kwargs):
    """
    Handle conversion when user upgrades to paid plan.

    Args:
        sender: Subscription model
        instance: Subscription instance
        created: Whether this is a new subscription
    """
    if created and instance.is_active and instance.plan.plan_type != 'free':
        # User upgraded to paid plan - attribute conversion
        try:
            ReferralService.attribute_conversion(instance.user)
        except Exception as e:
            # Log error but don't fail subscription creation
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to attribute conversion for {instance.user.email}: {str(e)}")
