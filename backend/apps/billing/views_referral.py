"""
Views for referral system.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings

from apps.billing.models_referral import ReferralCode, Referral, ReferralReward
from apps.billing.serializers_referral import (
    ReferralCodeSerializer,
    ReferralSerializer,
    ReferralRewardSerializer,
    TrackReferralSerializer,
)
from apps.billing.utils import get_client_ip
from services.referral_service import ReferralService


class ReferralViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing referrals.

    list: Get user's referrals
    retrieve: Get specific referral details
    stats: Get referral statistics
    my_code: Get user's referral code
    """
    serializer_class = ReferralSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return referrals made by current user."""
        return Referral.objects.filter(
            referrer=self.request.user
        ).select_related('referee', 'referral_code').order_by('-clicked_at')

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get comprehensive referral statistics.

        GET /api/v1/billing/referrals/stats/
        """
        stats = ReferralService.get_referral_stats(request.user)

        # Get referral link
        try:
            referral_code = request.user.referral_code
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
            referral_link = f"{frontend_url}/signup?ref={referral_code.code}"
        except:
            referral_link = None

        # Get active rewards
        active_rewards = ReferralService.get_active_rewards(request.user)
        rewards_serializer = ReferralRewardSerializer(active_rewards, many=True)

        # Calculate conversion rate
        conversion_rate = 0
        if stats['signups'] > 0:
            conversion_rate = (stats['conversions'] / stats['signups']) * 100

        response_data = {
            'code': stats['code'],
            'referral_link': referral_link,
            'clicks': stats['clicks'],
            'signups': stats['signups'],
            'conversions': stats['conversions'],
            'active_rewards': stats['active_rewards'],
            'total_rewards': stats['total_rewards'],
            'conversion_rate': round(conversion_rate, 2),
            'rewards': rewards_serializer.data,
        }

        return Response(response_data)

    @action(detail=False, methods=['get'])
    def my_code(self, request):
        """
        Get current user's referral code.

        GET /api/v1/billing/referrals/my_code/
        """
        try:
            referral_code = request.user.referral_code
            serializer = ReferralCodeSerializer(
                referral_code,
                context={'request': request}
            )
            return Response(serializer.data)
        except ReferralCode.DoesNotExist:
            # Create referral code if doesn't exist
            referral_code = ReferralService.create_referral_code(request.user)
            serializer = ReferralCodeSerializer(
                referral_code,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReferralRewardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing referral rewards.

    list: Get user's rewards
    retrieve: Get specific reward
    active: Get only active rewards
    """
    serializer_class = ReferralRewardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return rewards for current user."""
        return ReferralReward.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get only active rewards.

        GET /api/v1/billing/rewards/active/
        """
        active_rewards = ReferralService.get_active_rewards(request.user)
        serializer = self.get_serializer(active_rewards, many=True)

        # Also include bonus quota
        bonus = ReferralService.get_bonus_quota(request.user)

        return Response({
            'rewards': serializer.data,
            'bonus_quota': bonus,
        })

    @action(detail=False, methods=['get'])
    def bonus_quota(self, request):
        """
        Get current bonus quota from referral rewards.

        GET /api/v1/billing/rewards/bonus_quota/
        """
        bonus = ReferralService.get_bonus_quota(request.user)
        return Response(bonus)


@api_view(['POST'])
@permission_classes([AllowAny])
def track_referral_click(request):
    """
    Track referral link click.

    POST /api/v1/billing/referrals/track/
    Body: {
        "code": "DEVO-ALEX1234"
    }
    """
    serializer = TrackReferralSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    code = serializer.validated_data['code']

    try:
        referral_code = ReferralCode.objects.get(code=code)

        # Track click
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        referral = ReferralService.track_click(
            referral_code=referral_code,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        # Store referral ID in session for later attribution
        request.session['referral_id'] = str(referral.id)

        return Response({
            'success': True,
            'message': 'Referral tracked successfully',
            'referral_id': str(referral.id),
        })

    except ReferralCode.DoesNotExist:
        return Response(
            {'error': 'Invalid referral code'},
            status=status.HTTP_404_NOT_FOUND
        )
