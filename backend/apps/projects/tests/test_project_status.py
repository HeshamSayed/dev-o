"""
Unit tests for Project Status API endpoint.

GET /api/projects/{id}/status/
"""
import pytest
import uuid
from rest_framework import status
from apps.projects.tests.factories import ProjectFactory
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestProjectStatusAPI:
    """Tests for GET /api/projects/{id}/status/ endpoint."""

    def test_get_project_status_success(self, authenticated_client, user):
        """Test getting project status."""
        project = ProjectFactory(owner=user, status='in_progress')

        response = authenticated_client.get(f'/api/projects/{project.id}/status/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'in_progress'

    def test_get_project_status_includes_counts(self, authenticated_client, user):
        """Test status includes agent and task counts."""
        project = ProjectFactory(owner=user)

        response = authenticated_client.get(f'/api/projects/{project.id}/status/')

        assert response.status_code == status.HTTP_200_OK
        assert 'active_agents' in response.data
        assert 'pending_tasks' in response.data
        assert 'completed_tasks' in response.data

    def test_get_project_status_includes_activity(self, authenticated_client, user):
        """Test status includes recent activity."""
        project = ProjectFactory(owner=user)

        response = authenticated_client.get(f'/api/projects/{project.id}/status/')

        assert response.status_code == status.HTTP_200_OK
        assert 'recent_activity' in response.data

    def test_get_project_status_not_found(self, authenticated_client, user):
        """Test getting status for non-existent project."""
        fake_id = uuid.uuid4()

        response = authenticated_client.get(f'/api/projects/{fake_id}/status/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_project_status_other_user(self, authenticated_client, user):
        """Test cannot get status of another user's project."""
        other_user = UserFactory()
        project = ProjectFactory(owner=other_user)

        response = authenticated_client.get(f'/api/projects/{project.id}/status/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_project_status_unauthenticated(self, api_client, user):
        """Test unauthenticated access is denied."""
        project = ProjectFactory(owner=user)

        response = api_client.get(f'/api/projects/{project.id}/status/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
