"""
Views for billing and subscription management.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta

from .models import Plan, Subscription, UsageTracker, UsageLog
from .serializers import (
    PlanSerializer,
    SubscriptionSerializer,
    UsageTrackerSerializer,
    UsageLogSerializer,
    UsageSummarySerializer,
)
from services.usage_service import UsageService


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing pricing plans.

    list: Get all available pricing plans
    retrieve: Get details of a specific plan
    """
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer
    permission_classes = []  # Public endpoint

    def get_queryset(self):
        """Return active plans ordered by price."""
        return Plan.objects.filter(is_active=True).order_by('price_monthly')


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user subscriptions.

    list: Get user's subscription history
    retrieve: Get subscription details
    create: Create new subscription
    update: Update subscription
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return subscriptions for current user."""
        return Subscription.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current active subscription."""
        try:
            subscription = request.user.subscription
            serializer = self.get_serializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            # Return default free plan info
            free_plan = UsageService.get_user_plan(request.user)
            plan_serializer = PlanSerializer(free_plan)
            return Response({
                'subscription': None,
                'plan': plan_serializer.data,
                'message': 'User is on default Free plan'
            })

    def create(self, request, *args, **kwargs):
        """Create new subscription for user."""
        # Check if user already has subscription
        if hasattr(request.user, 'subscription'):
            return Response(
                {'error': 'User already has an active subscription'},
                status=status.HTTP_400_BAD_REQUEST
            )

        plan_id = request.data.get('plan_id')
        billing_cycle = request.data.get('billing_cycle', 'monthly')

        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response(
                {'error': 'Invalid plan ID'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create subscription
        now = timezone.now()
        period_end = now + timedelta(days=30 if billing_cycle == 'monthly' else 365)

        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            status='active',
            billing_cycle=billing_cycle,
            current_period_start=now,
            current_period_end=period_end,
        )

        serializer = self.get_serializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UsageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing usage data.

    list: Get usage history
    retrieve: Get specific usage window
    summary: Get current usage summary
    """
    serializer_class = UsageTrackerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return usage trackers for current user."""
        return UsageTracker.objects.filter(
            user=self.request.user
        ).order_by('-window_start')

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get current usage summary for user.

        Returns usage for current 2-hour window with limits and remaining quota.
        """
        summary = UsageService.get_usage_summary(request.user)
        serializer = UsageSummarySerializer(summary)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def current_window(self, request):
        """Get usage for current 2-hour window."""
        tracker = UsageService.get_or_create_usage_tracker(request.user)
        serializer = self.get_serializer(tracker)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Get usage history.

        Query params:
        - days: Number of days to look back (default: 7)
        - limit: Number of records to return (default: 50)
        """
        days = int(request.query_params.get('days', 7))
        limit = int(request.query_params.get('limit', 50))

        since = timezone.now() - timedelta(days=days)

        trackers = UsageTracker.objects.filter(
            user=request.user,
            window_start__gte=since
        ).order_by('-window_start')[:limit]

        serializer = self.get_serializer(trackers, many=True)
        return Response(serializer.data)


class UsageLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing detailed usage logs.

    list: Get usage logs
    retrieve: Get specific log entry
    """
    serializer_class = UsageLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return usage logs for current user."""
        queryset = UsageLog.objects.filter(user=self.request.user)

        # Filter by type
        usage_type = self.request.query_params.get('type')
        if usage_type:
            queryset = queryset.filter(usage_type=usage_type)

        # Filter by date range
        days = int(self.request.query_params.get('days', 7))
        since = timezone.now() - timedelta(days=days)
        queryset = queryset.filter(created_at__gte=since)

        return queryset.order_by('-created_at')
