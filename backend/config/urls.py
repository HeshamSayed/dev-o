"""URL configuration for AI Project Builder."""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.users import views as user_views
from apps.chat import views as chat_views
from apps.projects import views as project_views

# API Router
router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='user')
router.register(r'conversations', chat_views.ConversationViewSet, basename='conversation')
router.register(r'projects', project_views.ProjectViewSet, basename='project')

urlpatterns = [
    path('admin/', admin.site.urls),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # API v1
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/', include('apps.chat.urls')),
    path('api/v1/', include('apps.projects.urls')),
    path('api/v1/billing/', include('apps.billing.urls')),
]
