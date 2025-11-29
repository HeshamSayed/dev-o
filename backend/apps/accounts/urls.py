"""
URLs for accounts app.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    SubscriptionView,
    UsageStatsView,
    APIKeyListView,
    APIKeyDetailView
)

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserProfileView.as_view(), name='profile'),

    # Subscription & Usage
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('usage/', UsageStatsView.as_view(), name='usage'),

    # API Keys
    path('api-keys/', APIKeyListView.as_view(), name='api-key-list'),
    path('api-keys/<uuid:pk>/', APIKeyDetailView.as_view(), name='api-key-detail'),
]
