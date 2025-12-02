"""
URL configuration for billing app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, SubscriptionViewSet, UsageViewSet, UsageLogViewSet
from .views_referral import ReferralViewSet, ReferralRewardViewSet, track_referral_click

router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'usage', UsageViewSet, basename='usage')
router.register(r'logs', UsageLogViewSet, basename='usage-log')
router.register(r'referrals', ReferralViewSet, basename='referral')
router.register(r'rewards', ReferralRewardViewSet, basename='referral-reward')

urlpatterns = [
    path('', include(router.urls)),
    path('referrals/track/', track_referral_click, name='track-referral'),
]
