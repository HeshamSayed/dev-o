"""
Unit tests for Project List API endpoint.

GET /api/projects/
"""
import pytest
from rest_framework import status
from apps.projects.tests.factories import ProjectFactory
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestProjectListAPI:
    """Tests for GET /api/projects/ endpoint."""

    def test_list_projects_success(self, authenticated_client, user):
        """Test listing projects returns user's projects."""
        ProjectFactory.create_batch(3, owner=user)

        response = authenticated_client.get('/api/projects/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_list_projects_empty(self, authenticated_client, user):
        """Test listing projects when user has none."""
        response = authenticated_client.get('/api/projects/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_list_projects_only_own(self, authenticated_client, user):
        """Test user only sees their own projects."""
        ProjectFactory.create_batch(3, owner=user)
        other_user = UserFactory()
        ProjectFactory.create_batch(2, owner=other_user)

        response = authenticated_client.get('/api/projects/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_list_projects_ordered_by_updated_at(self, authenticated_client, user):
        """Test projects are ordered by updated_at descending."""
        p1 = ProjectFactory(owner=user, name='First')
        p2 = ProjectFactory(owner=user, name='Second')
        p3 = ProjectFactory(owner=user, name='Third')

        response = authenticated_client.get('/api/projects/')

        assert response.status_code == status.HTTP_200_OK
        # Most recently created should be first
        assert response.data[0]['name'] == 'Third'

    def test_list_projects_includes_counts(self, authenticated_client, user):
        """Test response includes agent and task counts."""
        project = ProjectFactory(owner=user)

        response = authenticated_client.get('/api/projects/')

        assert response.status_code == status.HTTP_200_OK
        assert 'agent_count' in response.data[0]
        assert 'task_count' in response.data[0]

    def test_list_projects_unauthenticated(self, api_client):
        """Test unauthenticated access is denied."""
        response = api_client.get('/api/projects/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
