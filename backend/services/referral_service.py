"""
Referral service for managing referral rewards and bonuses.
"""

from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from apps.billing.models_referral import ReferralCode, Referral, ReferralReward
from apps.billing.utils import generate_referral_code


class ReferralService:
    """Service for managing referrals and rewards."""

    @staticmethod
    def create_referral_code(user):
        """
        Create referral code for user.

        Args:
            user: User instance

        Returns:
            ReferralCode instance
        """
        code = generate_referral_code(user.username)
        referral_code = ReferralCode.objects.create(
            user=user,
            code=code
        )
        return referral_code

    @staticmethod
    def track_click(referral_code, ip_address=None, user_agent=''):
        """
        Track referral link click.

        Args:
            referral_code: ReferralCode instance
            ip_address: IP address of clicker
            user_agent: User agent string

        Returns:
            Referral instance
        """
        # Create referral tracking
        referral = Referral.objects.create(
            referrer=referral_code.user,
            referral_code=referral_code,
            status='clicked',
            ip_address=ip_address,
            user_agent=user_agent,
        )

        # Increment click count
        referral_code.clicks += 1
        referral_code.save()

        return referral

    @staticmethod
    @transaction.atomic
    def attribute_signup(referral_id, new_user):
        """
        Attribute signup to referral and give rewards.

        Args:
            referral_id: UUID of referral
            new_user: Newly created user

        Returns:
            Tuple of (referral, rewards_given)
        """
        try:
            referral = Referral.objects.get(id=referral_id)

            # Update referral
            referral.referee = new_user
            referral.status = 'signed_up'
            referral.signed_up_at = timezone.now()
            referral.save()

            # Update referral code stats
            referral.referral_code.signups += 1
            referral.referral_code.save()

            # Give rewards
            welcome_reward = ReferralService.create_welcome_bonus(new_user, referral)
            referrer_reward = ReferralService.create_signup_reward(
                referral.referrer, referral
            )

            return referral, [welcome_reward, referrer_reward]

        except Referral.DoesNotExist:
            return None, []

    @staticmethod
    @transaction.atomic
    def attribute_conversion(user):
        """
        Attribute conversion (upgrade to paid) to referral.

        Args:
            user: User who upgraded

        Returns:
            List of rewards created
        """
        try:
            # Find referral where user is referee
            referral = Referral.objects.get(
                referee=user,
                status='signed_up'
            )

            # Update referral
            referral.status = 'converted'
            referral.converted_at = timezone.now()
            referral.save()

            # Update referral code stats
            referral.referral_code.conversions += 1
            referral.referral_code.save()

            # Give conversion bonus to referrer
            reward = ReferralService.create_conversion_reward(
                referral.referrer, referral
            )

            return [reward] if reward else []

        except Referral.DoesNotExist:
            return []

    @staticmethod
    def create_welcome_bonus(user, referral):
        """
        Create welcome bonus for new user.

        Args:
            user: New user
            referral: Referral instance

        Returns:
            ReferralReward instance
        """
        now = timezone.now()

        reward = ReferralReward.objects.create(
            user=user,
            referral=referral,
            reward_type='extra_messages',
            status='active',
            amount=5,  # 5 extra messages
            description='Welcome bonus: +5 chat messages for your first month!',
            valid_from=now,
            valid_until=now + timedelta(days=30),
        )

        return reward

    @staticmethod
    def create_signup_reward(referrer, referral):
        """
        Create signup reward for referrer.

        Args:
            referrer: User who referred
            referral: Referral instance

        Returns:
            ReferralReward instance
        """
        now = timezone.now()

        reward = ReferralReward.objects.create(
            user=referrer,
            referral=referral,
            reward_type='extra_messages',
            status='active',
            amount=10,  # 10 extra messages
            description='Referral bonus: Friend signed up! +10 chat messages for 1 month',
            valid_from=now,
            valid_until=now + timedelta(days=30),
        )

        return reward

    @staticmethod
    def create_conversion_reward(referrer, referral):
        """
        Create conversion reward for referrer when referee upgrades.

        Args:
            referrer: User who referred
            referral: Referral instance

        Returns:
            ReferralReward instance
        """
        now = timezone.now()

        reward = ReferralReward.objects.create(
            user=referrer,
            referral=referral,
            reward_type='extra_requests',
            status='active',
            amount=25,  # 25 extra project requests
            description='Conversion bonus: Friend upgraded to paid! +25 project requests for 1 month',
            valid_from=now,
            valid_until=now + timedelta(days=30),
        )

        return reward

    @staticmethod
    def get_active_rewards(user):
        """
        Get all active rewards for user.

        Args:
            user: User instance

        Returns:
            QuerySet of active ReferralReward instances
        """
        now = timezone.now()

        return ReferralReward.objects.filter(
            user=user,
            status='active',
            valid_from__lte=now,
            valid_until__gte=now,
        )

    @staticmethod
    def get_referral_stats(user):
        """
        Get referral statistics for user.

        Args:
            user: User instance

        Returns:
            Dictionary with stats
        """
        try:
            referral_code = user.referral_code
        except:
            return {
                'code': None,
                'clicks': 0,
                'signups': 0,
                'conversions': 0,
                'active_rewards': 0,
                'total_rewards': 0,
            }

        active_rewards = ReferralService.get_active_rewards(user)

        return {
            'code': referral_code.code,
            'clicks': referral_code.clicks,
            'signups': referral_code.signups,
            'conversions': referral_code.conversions,
            'active_rewards': active_rewards.count(),
            'total_rewards': user.referral_rewards.count(),
        }

    @staticmethod
    def get_bonus_quota(user):
        """
        Calculate bonus quota from active rewards.

        Args:
            user: User instance

        Returns:
            Dictionary with bonus messages and requests
        """
        active_rewards = ReferralService.get_active_rewards(user)

        bonus = {
            'messages': 0,
            'requests': 0,
        }

        for reward in active_rewards:
            if reward.reward_type == 'extra_messages':
                bonus['messages'] += reward.amount
            elif reward.reward_type == 'extra_requests':
                bonus['requests'] += reward.amount

        return bonus

    @staticmethod
    def expire_old_rewards():
        """
        Expire rewards that have passed their validity period.

        Returns:
            Number of expired rewards
        """
        now = timezone.now()

        expired = ReferralReward.objects.filter(
            status='active',
            valid_until__lt=now,
        )

        count = expired.count()
        expired.update(status='expired')

        return count
