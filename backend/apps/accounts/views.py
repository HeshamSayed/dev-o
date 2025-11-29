"""
Account APIViews

Authentication and user management endpoints.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction

from .models import User, Subscription, UsageTracking, APIKey
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    SubscriptionSerializer,
    UsageTrackingSerializer,
    APIKeySerializer,
    APIKeyCreateSerializer
)


class RegisterView(APIView):
    """
    User registration endpoint.

    POST /api/auth/register/
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new user."""
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()

                # Create default subscription (or get if exists)
                Subscription.objects.get_or_create(
                    user=user,
                    defaults={
                        'tier': 'free',
                        'max_projects': 1,
                        'max_agents_per_project': 2,
                        'max_actions_per_day': 100,
                        'can_use_api_llms': False,
                        'can_use_custom_agents': False,
                        'is_active': True
                    }
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    User login endpoint.

    POST /api/auth/login/
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate user and return tokens."""
        # Accept both 'email' and 'username' for backwards compatibility
        username = request.data.get('email') or request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'error': 'Please provide both email/username and password'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({
                'error': 'Account is disabled'
            }, status=status.HTTP_403_FORBIDDEN)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


class LogoutView(APIView):
    """
    User logout endpoint.

    POST /api/auth/logout/
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Logout user by blacklisting refresh token."""
        try:
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({
                    'error': 'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    User profile endpoint.

    GET /api/auth/me/ - Get current user profile
    PATCH /api/auth/me/ - Update current user profile
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user profile."""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """Update current user profile."""
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionView(APIView):
    """
    User subscription endpoint.

    GET /api/auth/subscription/ - Get current subscription
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user's subscription."""
        try:
            subscription = request.user.subscription
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            return Response({
                'error': 'No subscription found'
            }, status=status.HTTP_404_NOT_FOUND)


class UsageStatsView(APIView):
    """
    User usage statistics endpoint.

    GET /api/auth/usage/ - Get current month's usage
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user's usage statistics."""
        from datetime import date

        today = date.today()

        usage, created = UsageTracking.objects.get_or_create(
            user=request.user,
            date=today
        )

        serializer = UsageTrackingSerializer(usage)
        return Response(serializer.data)


class APIKeyListView(APIView):
    """
    API Keys list endpoint.

    GET /api/auth/api-keys/ - List all API keys
    POST /api/auth/api-keys/ - Create new API key
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List user's API keys."""
        api_keys = APIKey.objects.filter(user=request.user)
        serializer = APIKeySerializer(api_keys, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create new API key."""
        serializer = APIKeyCreateSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            api_key = serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIKeyDetailView(APIView):
    """
    API Key detail endpoint.

    DELETE /api/auth/api-keys/{id}/ - Delete API key
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """Delete an API key."""
        try:
            api_key = APIKey.objects.get(id=pk, user=request.user)
            api_key.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except APIKey.DoesNotExist:
            return Response({
                'error': 'API key not found'
            }, status=status.HTTP_404_NOT_FOUND)
