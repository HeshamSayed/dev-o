"""
Unit tests for Project Delete API endpoint.

DELETE /api/projects/{id}/
"""
import pytest
import uuid
from rest_framework import status
from apps.projects.models import Project, ProjectCheckpoint
from apps.projects.tests.factories import ProjectFactory, ProjectCheckpointFactory
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestProjectDeleteAPI:
    """Tests for DELETE /api/projects/{id}/ endpoint."""

    def test_delete_project_success(self, authenticated_client, user):
        """Test deleting a project."""
        project = ProjectFactory(owner=user)
        project_id = project.id

        response = authenticated_client.delete(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Project.objects.filter(id=project_id).exists()

    def test_delete_project_cascades(self, authenticated_client, user):
        """Test deleting project cascades to related objects."""
        project = ProjectFactory(owner=user)
        checkpoint = ProjectCheckpointFactory(project=project)
        checkpoint_id = checkpoint.id

        response = authenticated_client.delete(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ProjectCheckpoint.objects.filter(id=checkpoint_id).exists()

    def test_delete_project_not_found(self, authenticated_client, user):
        """Test deleting non-existent project returns 404."""
        fake_id = uuid.uuid4()

        response = authenticated_client.delete(f'/api/projects/{fake_id}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_project_other_user(self, authenticated_client, user):
        """Test cannot delete another user's project."""
        other_user = UserFactory()
        project = ProjectFactory(owner=other_user)

        response = authenticated_client.delete(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        # Verify project still exists
        assert Project.objects.filter(id=project.id).exists()

    def test_delete_project_unauthenticated(self, api_client, user):
        """Test unauthenticated access is denied."""
        project = ProjectFactory(owner=user)

        response = api_client.delete(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
