"""
Subscription management API views.
"""
import stripe
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from apps.accounts.stripe_service import StripeService, UsageLimitService


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subscription(request):
    """
    Create a new subscription.

    POST /api/subscription/create/
    Body: {
        "tier": "pro|team|enterprise",
        "payment_method_id": "pm_xxx"
    }
    """
    user = request.user
    tier = request.data.get('tier')
    payment_method_id = request.data.get('payment_method_id')

    if tier not in ['pro', 'team', 'enterprise']:
        return Response(
            {'error': 'Invalid tier'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = StripeService.create_subscription(
            user=user,
            tier=tier,
            payment_method_id=payment_method_id
        )

        return Response(result, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    """
    Cancel current subscription.

    POST /api/subscription/cancel/
    """
    user = request.user

    try:
        success = StripeService.cancel_subscription(user)

        if success:
            return Response(
                {'message': 'Subscription will be cancelled at period end'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'No active subscription'},
                status=status.HTTP_400_BAD_REQUEST
            )

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reactivate_subscription(request):
    """
    Reactivate cancelled subscription.

    POST /api/subscription/reactivate/
    """
    user = request.user

    try:
        success = StripeService.reactivate_subscription(user)

        if success:
            return Response(
                {'message': 'Subscription reactivated'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'No subscription to reactivate'},
                status=status.HTTP_400_BAD_REQUEST
            )

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_subscription_tier(request):
    """
    Change subscription tier.

    POST /api/subscription/change-tier/
    Body: {
        "tier": "pro|team|enterprise"
    }
    """
    user = request.user
    new_tier = request.data.get('tier')

    if new_tier not in ['pro', 'team', 'enterprise']:
        return Response(
            {'error': 'Invalid tier'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = StripeService.change_subscription_tier(user, new_tier)
        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscription_status(request):
    """
    Get current subscription status.

    GET /api/subscription/status/
    """
    user = request.user

    try:
        status_data = StripeService.get_subscription_status(user)
        return Response(status_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usage_limits(request):
    """
    Get current usage and limits.

    GET /api/subscription/usage/
    """
    user = request.user
    subscription = user.subscription

    # Get current usage
    from apps.accounts.models import UsageTracking
    from datetime import date

    today = date.today()
    usage, _ = UsageTracking.objects.get_or_create(
        user=user,
        date=today,
        defaults={'agent_actions': 0}
    )

    # Get counts
    project_count = user.owned_projects.count()

    return Response({
        'subscription': {
            'tier': subscription.tier,
            'is_active': subscription.is_active,
        },
        'limits': {
            'max_projects': subscription.max_projects,
            'max_agents_per_project': subscription.max_agents_per_project,
            'max_actions_per_day': subscription.max_actions_per_day,
            'can_use_api_llms': subscription.can_use_api_llms,
        },
        'usage': {
            'current_projects': project_count,
            'actions_today': usage.agent_actions,
            'tokens_today': usage.llm_tokens_used,
            'files_generated_today': usage.files_generated,
        },
        'remaining': {
            'projects': max(0, subscription.max_projects - project_count),
            'actions_today': max(0, subscription.max_actions_per_day - usage.agent_actions),
        }
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook(request):
    """
    Handle Stripe webhook events.

    POST /api/webhook/stripe/
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    try:
        StripeService.handle_webhook(event)
        return HttpResponse(status=200)
    except Exception as e:
        # Log error but return 200 to acknowledge receipt
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Webhook handling error: {str(e)}")
        return HttpResponse(status=200)
