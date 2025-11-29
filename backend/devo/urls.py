"""
URL configuration for DEVO project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

# API Router
router = routers.DefaultRouter()

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API
    path('api/', include(router.urls)),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/projects/', include('apps.projects.urls')),
    path('api/agents/', include('apps.agents.urls')),
    path('api/tasks/', include('apps.tasks.urls')),
    path('api/code/', include('apps.code.urls')),
    path('api/context/', include('apps.context.urls')),

    # Health check
    path('health/', lambda request: __import__('django.http').JsonResponse({'status': 'ok'})),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns = [
            path('__debug__/', include('debug_toolbar.urls')),
        ] + urlpatterns

# Custom admin site settings
admin.site.site_header = 'DEVO Administration'
admin.site.site_title = 'DEVO Admin'
admin.site.index_title = 'Welcome to DEVO Administration'
