"""
Unit tests for Project Detail API endpoint.

GET /api/projects/{id}/
"""
import pytest
import uuid
from rest_framework import status
from apps.projects.tests.factories import ProjectFactory
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestProjectDetailAPI:
    """Tests for GET /api/projects/{id}/ endpoint."""

    def test_get_project_success(self, authenticated_client, user):
        """Test retrieving a project."""
        project = ProjectFactory(owner=user)

        response = authenticated_client.get(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == project.name
        assert response.data['description'] == project.description

    def test_get_project_includes_statistics(self, authenticated_client, user):
        """Test project detail includes statistics."""
        project = ProjectFactory(owner=user)

        response = authenticated_client.get(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert 'statistics' in response.data
        stats = response.data['statistics']
        assert 'total_agents' in stats
        assert 'total_tasks' in stats
        assert 'completed_tasks' in stats

    def test_get_project_includes_agents(self, authenticated_client, user):
        """Test project detail includes agents list."""
        project = ProjectFactory(owner=user)

        response = authenticated_client.get(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert 'agents' in response.data

    def test_get_project_includes_recent_tasks(self, authenticated_client, user):
        """Test project detail includes recent tasks."""
        project = ProjectFactory(owner=user)

        response = authenticated_client.get(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert 'recent_tasks' in response.data

    def test_get_project_not_found(self, authenticated_client, user):
        """Test getting non-existent project returns 404."""
        fake_id = uuid.uuid4()

        response = authenticated_client.get(f'/api/projects/{fake_id}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'] == 'Project not found'

    def test_get_project_other_user(self, authenticated_client, user):
        """Test cannot access another user's project."""
        other_user = UserFactory()
        project = ProjectFactory(owner=other_user)

        response = authenticated_client.get(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_project_unauthenticated(self, api_client, user):
        """Test unauthenticated access is denied."""
        project = ProjectFactory(owner=user)

        response = api_client.get(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
