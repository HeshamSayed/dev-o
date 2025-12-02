"""
Usage tracking service with 2-hour reset windows.

Smart move! 2-hour resets make users come back frequently and get hooked on the platform.
"""

from datetime import datetime, timedelta
from typing import Tuple, Optional
from django.utils import timezone
from django.db import transaction
from django.contrib.auth import get_user_model
from apps.billing.models import Plan, Subscription, UsageTracker, UsageLog

User = get_user_model()


class UsageService:
    """Service for tracking and enforcing usage limits with 2-hour windows."""

    @staticmethod
    def get_current_window() -> Tuple[datetime, datetime]:
        """
        Calculate current 2-hour window.

        Windows: 00:00-02:00, 02:00-04:00, 04:00-06:00, ..., 22:00-00:00
        Total: 12 windows per day

        Returns:
            Tuple of (window_start, window_end)
        """
        now = timezone.now()

        # Get the current hour
        current_hour = now.hour

        # Calculate window start hour (round down to nearest even hour)
        window_start_hour = (current_hour // 2) * 2

        # Create window start (same day, calculated hour, 00:00:00)
        window_start = now.replace(
            hour=window_start_hour,
            minute=0,
            second=0,
            microsecond=0
        )

        # Window end is 2 hours later
        window_end = window_start + timedelta(hours=2)

        return window_start, window_end

    @staticmethod
    def get_or_create_usage_tracker(user: User) -> UsageTracker:
        """
        Get or create UsageTracker for current 2-hour window.

        Args:
            user: User to track usage for

        Returns:
            UsageTracker instance for current window
        """
        window_start, window_end = UsageService.get_current_window()

        tracker, created = UsageTracker.objects.get_or_create(
            user=user,
            window_start=window_start,
            defaults={
                'window_end': window_end,
            }
        )

        return tracker

    @staticmethod
    def get_user_plan(user: User) -> Plan:
        """
        Get user's current plan or default to Free plan.

        Args:
            user: User to get plan for

        Returns:
            Plan instance
        """
        try:
            subscription = user.subscription
            if subscription.is_active:
                return subscription.plan
        except Subscription.DoesNotExist:
            pass

        # Default to Free plan
        free_plan, _ = Plan.objects.get_or_create(
            plan_type='free',
            defaults={
                'name': 'Free',
                'price_monthly': 0,
                'price_yearly': 0,
                'messages_per_window': 10,
                'max_conversations': 5,
                'context_window': 4096,
                'max_active_projects': 1,
                'max_archived_projects': 0,
                'max_files_per_project': 10,
                'project_requests_per_window': 2,
                'available_agents': ['Marcus - Backend Lead'],
                'max_concurrent_agents': 1,
                'storage_limit_mb': 10,
                'max_file_size_kb': 100,
                'retention_days': 7,
                'model_tier': 'basic',
                'max_output_tokens': 1024,
                'requests_per_minute': 2,
                'max_concurrent_connections': 1,
                'queue_priority': 0,
                'has_thinking_mode': False,
                'has_download': False,
                'has_git_integration': False,
                'has_api_access': False,
                'has_chat_search': False,
            }
        )
        return free_plan

    @staticmethod
    def check_chat_limit(user: User) -> Tuple[bool, int, int]:
        """
        Check if user can send chat message in current window.
        Includes referral bonus quota.

        Args:
            user: User to check limit for

        Returns:
            Tuple of (can_send, used, limit)
        """
        plan = UsageService.get_user_plan(user)
        tracker = UsageService.get_or_create_usage_tracker(user)

        used = tracker.chat_messages_used
        limit = plan.messages_per_window

        # Add referral bonuses
        try:
            from services.referral_service import ReferralService
            bonus = ReferralService.get_bonus_quota(user)
            if limit != -1:  # Don't add to unlimited
                limit += bonus['messages']
        except:
            pass  # If referral service not available, continue without bonus

        # -1 means unlimited
        can_send = (limit == -1) or (used < limit)

        return can_send, used, limit

    @staticmethod
    def check_project_request_limit(user: User) -> Tuple[bool, int, int]:
        """
        Check if user can make project request in current window.
        Includes referral bonus quota.

        Args:
            user: User to check limit for

        Returns:
            Tuple of (can_request, used, limit)
        """
        plan = UsageService.get_user_plan(user)
        tracker = UsageService.get_or_create_usage_tracker(user)

        used = tracker.project_requests_used
        limit = plan.project_requests_per_window

        # Add referral bonuses
        try:
            from services.referral_service import ReferralService
            bonus = ReferralService.get_bonus_quota(user)
            if limit != -1:  # Don't add to unlimited
                limit += bonus['requests']
        except:
            pass  # If referral service not available, continue without bonus

        # -1 means unlimited
        can_request = (limit == -1) or (used < limit)

        return can_request, used, limit

    @staticmethod
    @transaction.atomic
    def record_chat_message(
        user: User,
        conversation_id: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        model_used: str = 'default',
        duration_ms: int = 0,
        estimated_cost: float = 0.0
    ) -> UsageTracker:
        """
        Record chat message usage.

        Args:
            user: User who sent message
            conversation_id: UUID of conversation
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model_used: AI model used
            duration_ms: Request duration in milliseconds
            estimated_cost: Estimated cost of request

        Returns:
            Updated UsageTracker
        """
        tracker = UsageService.get_or_create_usage_tracker(user)

        # Update tracker
        tracker.chat_messages_used += 1
        tracker.chat_tokens_used += (input_tokens + output_tokens)
        tracker.save()

        # Create usage log
        UsageLog.objects.create(
            user=user,
            usage_type='chat_message',
            conversation_id=conversation_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=estimated_cost,
            model_used=model_used,
            duration_ms=duration_ms
        )

        return tracker

    @staticmethod
    @transaction.atomic
    def record_project_request(
        user: User,
        project_id: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        model_used: str = 'default',
        duration_ms: int = 0,
        estimated_cost: float = 0.0
    ) -> UsageTracker:
        """
        Record project request usage.

        Args:
            user: User who made request
            project_id: UUID of project
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model_used: AI model used
            duration_ms: Request duration in milliseconds
            estimated_cost: Estimated cost of request

        Returns:
            Updated UsageTracker
        """
        tracker = UsageService.get_or_create_usage_tracker(user)

        # Update tracker
        tracker.project_requests_used += 1
        tracker.project_tokens_used += (input_tokens + output_tokens)
        tracker.save()

        # Create usage log
        UsageLog.objects.create(
            user=user,
            usage_type='project_request',
            project_id=project_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=estimated_cost,
            model_used=model_used,
            duration_ms=duration_ms
        )

        return tracker

    @staticmethod
    def get_usage_summary(user: User) -> dict:
        """
        Get usage summary for current window.

        Args:
            user: User to get summary for

        Returns:
            Dictionary with usage stats
        """
        plan = UsageService.get_user_plan(user)
        tracker = UsageService.get_or_create_usage_tracker(user)
        window_start, window_end = UsageService.get_current_window()

        # Calculate time until reset
        now = timezone.now()
        time_until_reset = window_end - now
        minutes_until_reset = int(time_until_reset.total_seconds() / 60)

        return {
            'plan': {
                'name': plan.name,
                'type': plan.plan_type,
            },
            'window': {
                'start': window_start,
                'end': window_end,
                'minutes_until_reset': minutes_until_reset,
            },
            'chat': {
                'used': tracker.chat_messages_used,
                'limit': plan.messages_per_window,
                'remaining': (plan.messages_per_window - tracker.chat_messages_used) if plan.messages_per_window != -1 else -1,
            },
            'projects': {
                'used': tracker.project_requests_used,
                'limit': plan.project_requests_per_window,
                'remaining': (plan.project_requests_per_window - tracker.project_requests_used) if plan.project_requests_per_window != -1 else -1,
            },
            'features': {
                'thinking_mode': plan.has_thinking_mode,
                'download': plan.has_download,
                'git_integration': plan.has_git_integration,
                'api_access': plan.has_api_access,
                'chat_search': plan.has_chat_search,
            }
        }

    @staticmethod
    def check_feature_access(user: User, feature: str) -> bool:
        """
        Check if user has access to a feature.

        Args:
            user: User to check
            feature: Feature name (thinking_mode, download, git_integration, api_access, chat_search)

        Returns:
            True if user has access
        """
        plan = UsageService.get_user_plan(user)

        feature_map = {
            'thinking_mode': plan.has_thinking_mode,
            'download': plan.has_download,
            'git_integration': plan.has_git_integration,
            'api_access': plan.has_api_access,
            'chat_search': plan.has_chat_search,
        }

        return feature_map.get(feature, False)

    @staticmethod
    def get_available_agents(user: User) -> list:
        """
        Get list of agents available to user.

        Args:
            user: User to check

        Returns:
            List of agent names
        """
        plan = UsageService.get_user_plan(user)
        return plan.available_agents
