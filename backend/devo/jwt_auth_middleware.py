"""
JWT Authentication Middleware for Django Channels WebSocket connections.
"""
import logging
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from apps.accounts.models import User
from urllib.parse import parse_qs

logger = logging.getLogger(__name__)


@database_sync_to_async
def get_user_from_token(token_string):
    """Get user from JWT token."""
    try:
        access_token = AccessToken(token_string)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)
        logger.info(f"[JWT] Successfully authenticated user: {user.email}")
        return user
    except Exception as e:
        logger.error(f"[JWT] Token validation failed: {str(e)}")
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """
    JWT authentication middleware for WebSocket connections.

    Accepts token via:
    1. Query parameter: ?token=<jwt_token>
    2. Sec-WebSocket-Protocol header
    """

    async def __call__(self, scope, receive, send):
        import sys
        # Extract token from query string
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]

        # DEBUG: Log token extraction
        sys.stderr.write(f"[JWT DEBUG] Query string: {query_string}\n")
        sys.stderr.write(f"[JWT DEBUG] Query params: {query_params}\n")
        sys.stderr.write(f"[JWT DEBUG] Token extracted from query: {token[:20] if token else None}\n")
        sys.stderr.flush()

        # If not in query, check subprotocols (Sec-WebSocket-Protocol header)
        if not token:
            subprotocols = scope.get('subprotocols', [])
            sys.stderr.write(f"[JWT DEBUG] No token in query, checking subprotocols: {subprotocols}\n")
            sys.stderr.flush()
            for protocol in subprotocols:
                if protocol.startswith('token.'):
                    token = protocol.replace('token.', '')
                    break

        # Authenticate user
        if token:
            scope['user'] = await get_user_from_token(token)
            sys.stderr.write(f"[JWT DEBUG] User authenticated: {scope['user']}\n")
            sys.stderr.flush()
        else:
            scope['user'] = AnonymousUser()
            sys.stderr.write(f"[JWT DEBUG] No token found, setting AnonymousUser\n")
            sys.stderr.flush()

        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    """Helper function to wrap middleware."""
    return JWTAuthMiddleware(inner)
