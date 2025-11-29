"""
Stripe integration service for subscription management.

Handles Stripe API calls, webhook processing, and subscription lifecycle.
"""
import stripe
from typing import Dict, Any, Optional
from django.conf import settings
from django.utils import timezone

from apps.accounts.models import User, Subscription

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Service for handling Stripe operations."""

    # Subscription tier to Stripe price mapping
    TIER_PRICES = {
        'free': None,  # No Stripe subscription
        'pro': settings.STRIPE_PRO_PRICE_ID if hasattr(settings, 'STRIPE_PRO_PRICE_ID') else None,
        'team': settings.STRIPE_TEAM_PRICE_ID if hasattr(settings, 'STRIPE_TEAM_PRICE_ID') else None,
        'enterprise': settings.STRIPE_ENTERPRISE_PRICE_ID if hasattr(settings, 'STRIPE_ENTERPRISE_PRICE_ID') else None,
    }

    @classmethod
    def create_customer(cls, user: User) -> str:
        """
        Create a Stripe customer for a user.

        Args:
            user: User instance

        Returns:
            Stripe customer ID
        """
        customer = stripe.Customer.create(
            email=user.email,
            name=user.get_full_name() or user.username,
            metadata={
                'user_id': str(user.id),
                'username': user.username,
            }
        )

        return customer.id

    @classmethod
    def create_subscription(
        cls,
        user: User,
        tier: str,
        payment_method_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a subscription for a user.

        Args:
            user: User instance
            tier: Subscription tier (pro, team, enterprise)
            payment_method_id: Stripe payment method ID

        Returns:
            Subscription data
        """
        # Get or create Stripe customer
        subscription = user.subscription

        if not subscription.stripe_customer_id:
            customer_id = cls.create_customer(user)
            subscription.stripe_customer_id = customer_id
            subscription.save()
        else:
            customer_id = subscription.stripe_customer_id

        # Attach payment method if provided
        if payment_method_id:
            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=customer_id,
            )

            # Set as default payment method
            stripe.Customer.modify(
                customer_id,
                invoice_settings={
                    'default_payment_method': payment_method_id,
                },
            )

        # Get price ID for tier
        price_id = cls.TIER_PRICES.get(tier)
        if not price_id:
            raise ValueError(f"Invalid tier or no price configured: {tier}")

        # Create subscription
        stripe_subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
        )

        # Update local subscription
        subscription.stripe_subscription_id = stripe_subscription.id
        subscription.tier = tier
        subscription.is_active = stripe_subscription.status in ['active', 'trialing']
        subscription.save()

        return {
            'subscription_id': stripe_subscription.id,
            'client_secret': stripe_subscription.latest_invoice.payment_intent.client_secret,
            'status': stripe_subscription.status,
        }

    @classmethod
    def cancel_subscription(cls, user: User) -> bool:
        """
        Cancel a user's subscription.

        Args:
            user: User instance

        Returns:
            True if cancelled successfully
        """
        subscription = user.subscription

        if not subscription.stripe_subscription_id:
            return False

        # Cancel at period end
        stripe.Subscription.modify(
            subscription.stripe_subscription_id,
            cancel_at_period_end=True,
        )

        return True

    @classmethod
    def reactivate_subscription(cls, user: User) -> bool:
        """
        Reactivate a cancelled subscription.

        Args:
            user: User instance

        Returns:
            True if reactivated successfully
        """
        subscription = user.subscription

        if not subscription.stripe_subscription_id:
            return False

        # Remove cancellation
        stripe.Subscription.modify(
            subscription.stripe_subscription_id,
            cancel_at_period_end=False,
        )

        return True

    @classmethod
    def change_subscription_tier(cls, user: User, new_tier: str) -> Dict[str, Any]:
        """
        Change a user's subscription tier.

        Args:
            user: User instance
            new_tier: New subscription tier

        Returns:
            Updated subscription data
        """
        subscription = user.subscription

        if not subscription.stripe_subscription_id:
            raise ValueError("No active subscription")

        # Get new price ID
        new_price_id = cls.TIER_PRICES.get(new_tier)
        if not new_price_id:
            raise ValueError(f"Invalid tier: {new_tier}")

        # Get current subscription
        stripe_subscription = stripe.Subscription.retrieve(
            subscription.stripe_subscription_id
        )

        # Update subscription
        stripe.Subscription.modify(
            subscription.stripe_subscription_id,
            items=[{
                'id': stripe_subscription['items']['data'][0].id,
                'price': new_price_id,
            }],
            proration_behavior='always_invoice',
        )

        # Update local subscription
        subscription.tier = new_tier
        subscription.save()

        return {
            'tier': new_tier,
            'status': 'updated',
        }

    @classmethod
    def get_subscription_status(cls, user: User) -> Dict[str, Any]:
        """
        Get current subscription status.

        Args:
            user: User instance

        Returns:
            Subscription status data
        """
        subscription = user.subscription

        if not subscription.stripe_subscription_id:
            return {
                'tier': subscription.tier,
                'status': 'inactive',
                'is_active': False,
            }

        # Fetch from Stripe
        stripe_subscription = stripe.Subscription.retrieve(
            subscription.stripe_subscription_id
        )

        return {
            'tier': subscription.tier,
            'status': stripe_subscription.status,
            'is_active': stripe_subscription.status in ['active', 'trialing'],
            'current_period_end': stripe_subscription.current_period_end,
            'cancel_at_period_end': stripe_subscription.cancel_at_period_end,
        }

    @classmethod
    def handle_webhook(cls, event: Dict[str, Any]) -> bool:
        """
        Handle Stripe webhook event.

        Args:
            event: Stripe event data

        Returns:
            True if handled successfully
        """
        event_type = event['type']

        if event_type == 'customer.subscription.created':
            return cls._handle_subscription_created(event['data']['object'])

        elif event_type == 'customer.subscription.updated':
            return cls._handle_subscription_updated(event['data']['object'])

        elif event_type == 'customer.subscription.deleted':
            return cls._handle_subscription_deleted(event['data']['object'])

        elif event_type == 'invoice.payment_succeeded':
            return cls._handle_payment_succeeded(event['data']['object'])

        elif event_type == 'invoice.payment_failed':
            return cls._handle_payment_failed(event['data']['object'])

        return True

    @classmethod
    def _handle_subscription_created(cls, subscription_data: Dict) -> bool:
        """Handle subscription.created event."""
        subscription_id = subscription_data['id']

        # Find subscription by Stripe ID
        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=subscription_id
            )
            subscription.is_active = subscription_data['status'] in ['active', 'trialing']
            subscription.save()
            return True
        except Subscription.DoesNotExist:
            return False

    @classmethod
    def _handle_subscription_updated(cls, subscription_data: Dict) -> bool:
        """Handle subscription.updated event."""
        subscription_id = subscription_data['id']

        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=subscription_id
            )
            subscription.is_active = subscription_data['status'] in ['active', 'trialing']

            # Update expiration date
            if subscription_data.get('current_period_end'):
                subscription.expires_at = timezone.datetime.fromtimestamp(
                    subscription_data['current_period_end'],
                    tz=timezone.utc
                )

            subscription.save()
            return True
        except Subscription.DoesNotExist:
            return False

    @classmethod
    def _handle_subscription_deleted(cls, subscription_data: Dict) -> bool:
        """Handle subscription.deleted event."""
        subscription_id = subscription_data['id']

        try:
            subscription = Subscription.objects.get(
                stripe_subscription_id=subscription_id
            )
            subscription.is_active = False
            subscription.tier = 'free'
            subscription.save()
            return True
        except Subscription.DoesNotExist:
            return False

    @classmethod
    def _handle_payment_succeeded(cls, invoice_data: Dict) -> bool:
        """Handle invoice.payment_succeeded event."""
        customer_id = invoice_data.get('customer')

        if customer_id:
            try:
                subscription = Subscription.objects.get(
                    stripe_customer_id=customer_id
                )
                subscription.is_active = True
                subscription.save()
                return True
            except Subscription.DoesNotExist:
                return False

        return True

    @classmethod
    def _handle_payment_failed(cls, invoice_data: Dict) -> bool:
        """Handle invoice.payment_failed event."""
        customer_id = invoice_data.get('customer')

        if customer_id:
            try:
                subscription = Subscription.objects.get(
                    stripe_customer_id=customer_id
                )
                # Don't immediately deactivate, Stripe will retry
                # Just log the failure
                return True
            except Subscription.DoesNotExist:
                return False

        return True


class UsageLimitService:
    """Service for checking and enforcing usage limits."""

    @classmethod
    def check_project_limit(cls, user: User) -> bool:
        """
        Check if user can create more projects.

        Args:
            user: User instance

        Returns:
            True if within limit
        """
        subscription = user.subscription
        current_count = user.owned_projects.count()

        return current_count < subscription.max_projects

    @classmethod
    def check_agent_limit(cls, project) -> bool:
        """
        Check if project can add more agents.

        Args:
            project: Project instance

        Returns:
            True if within limit
        """
        subscription = project.owner.subscription
        current_count = project.agent_instances.count()

        return current_count < subscription.max_agents_per_project

    @classmethod
    def check_daily_action_limit(cls, user: User) -> bool:
        """
        Check if user has exceeded daily action limit.

        Args:
            user: User instance

        Returns:
            True if within limit
        """
        from apps.accounts.models import UsageTracking
        from datetime import date

        subscription = user.subscription
        today = date.today()

        usage, _ = UsageTracking.objects.get_or_create(
            user=user,
            date=today,
            defaults={'agent_actions': 0}
        )

        return usage.agent_actions < subscription.max_actions_per_day

    @classmethod
    def increment_action_count(cls, user: User) -> None:
        """
        Increment user's action count for today.

        Args:
            user: User instance
        """
        from apps.accounts.models import UsageTracking
        from datetime import date
        from django.db.models import F

        today = date.today()

        UsageTracking.objects.update_or_create(
            user=user,
            date=today,
            defaults={'agent_actions': 0}
        )

        UsageTracking.objects.filter(
            user=user,
            date=today
        ).update(agent_actions=F('agent_actions') + 1)
