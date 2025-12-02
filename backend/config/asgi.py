"""
ASGI config for AI Project Builder.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django ASGI application early to ensure AppRegistry is populated
django_asgi_app = get_asgi_application()

# Import routing and middleware after django_asgi_app is initialized
from apps.chat.routing import websocket_urlpatterns as chat_patterns
from apps.projects.routing import websocket_urlpatterns as project_patterns
from apps.chat.middleware import JWTAuthMiddleware

# Combine all websocket URL patterns
websocket_urlpatterns = chat_patterns + project_patterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        JWTAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
