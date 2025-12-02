"""Agent views."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Agent, AgentAssignment
from .serializers import AgentSerializer, AgentAssignmentSerializer


class AgentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing agents (read-only for users)."""

    permission_classes = [IsAuthenticated]
    serializer_class = AgentSerializer
    queryset = Agent.objects.filter(is_active=True)

    def get_permissions(self):
        # Only admins can create/update/delete agents
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()
