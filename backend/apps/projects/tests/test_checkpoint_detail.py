"""
Unit tests for Checkpoint Detail API endpoint.

GET/DELETE /api/projects/{project_id}/checkpoints/{checkpoint_id}/
"""
import pytest
import uuid
from rest_framework import status
from apps.projects.models import ProjectCheckpoint
from apps.projects.tests.factories import ProjectFactory, ProjectCheckpointFactory
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestCheckpointDetailAPI:
    """Tests for GET/DELETE /api/projects/{id}/checkpoints/{checkpoint_id}/ endpoint."""

    def test_get_checkpoint_success(self, authenticated_client, user):
        """Test getting checkpoint details."""
        project = ProjectFactory(owner=user)
        checkpoint = ProjectCheckpointFactory(project=project)

        response = authenticated_client.get(
            f'/api/projects/{project.id}/checkpoints/{checkpoint.id}/'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == checkpoint.name
        assert 'state_snapshot' in response.data

    def test_get_checkpoint_not_found(self, authenticated_client, user):
        """Test getting non-existent checkpoint."""
        project = ProjectFactory(owner=user)
        fake_id = uuid.uuid4()

        response = authenticated_client.get(
            f'/api/projects/{project.id}/checkpoints/{fake_id}/'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_checkpoint_wrong_project(self, authenticated_client, user):
        """Test checkpoint must belong to specified project."""
        project1 = ProjectFactory(owner=user)
        project2 = ProjectFactory(owner=user)
        checkpoint = ProjectCheckpointFactory(project=project1)

        response = authenticated_client.get(
            f'/api/projects/{project2.id}/checkpoints/{checkpoint.id}/'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_checkpoint_other_user(self, authenticated_client, user):
        """Test cannot get checkpoint of another user's project."""
        other_user = UserFactory()
        project = ProjectFactory(owner=other_user)
        checkpoint = ProjectCheckpointFactory(project=project)

        response = authenticated_client.get(
            f'/api/projects/{project.id}/checkpoints/{checkpoint.id}/'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_checkpoint_success(self, authenticated_client, user):
        """Test deleting a checkpoint."""
        project = ProjectFactory(owner=user)
        checkpoint = ProjectCheckpointFactory(project=project)
        checkpoint_id = checkpoint.id

        response = authenticated_client.delete(
            f'/api/projects/{project.id}/checkpoints/{checkpoint.id}/'
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not ProjectCheckpoint.objects.filter(id=checkpoint_id).exists()

    def test_delete_checkpoint_not_found(self, authenticated_client, user):
        """Test deleting non-existent checkpoint."""
        project = ProjectFactory(owner=user)
        fake_id = uuid.uuid4()

        response = authenticated_client.delete(
            f'/api/projects/{project.id}/checkpoints/{fake_id}/'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_checkpoint_other_user(self, authenticated_client, user):
        """Test cannot delete checkpoint of another user's project."""
        other_user = UserFactory()
        project = ProjectFactory(owner=other_user)
        checkpoint = ProjectCheckpointFactory(project=project)

        response = authenticated_client.delete(
            f'/api/projects/{project.id}/checkpoints/{checkpoint.id}/'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        # Verify checkpoint still exists
        assert ProjectCheckpoint.objects.filter(id=checkpoint.id).exists()
