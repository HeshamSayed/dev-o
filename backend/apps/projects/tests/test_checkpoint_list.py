"""
Unit tests for Checkpoint List API endpoint.

GET/POST /api/projects/{id}/checkpoints/
"""
import pytest
import uuid
from rest_framework import status
from apps.projects.tests.factories import ProjectFactory, ProjectCheckpointFactory
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestCheckpointListAPI:
    """Tests for GET/POST /api/projects/{id}/checkpoints/ endpoint."""

    def test_list_checkpoints_success(self, authenticated_client, user):
        """Test listing project checkpoints."""
        project = ProjectFactory(owner=user)
        ProjectCheckpointFactory.create_batch(3, project=project)

        response = authenticated_client.get(f'/api/projects/{project.id}/checkpoints/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_list_checkpoints_empty(self, authenticated_client, user):
        """Test listing checkpoints when project has none."""
        project = ProjectFactory(owner=user)

        response = authenticated_client.get(f'/api/projects/{project.id}/checkpoints/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_list_checkpoints_ordered_by_date(self, authenticated_client, user):
        """Test checkpoints are ordered by created_at descending."""
        project = ProjectFactory(owner=user)
        ProjectCheckpointFactory(project=project, name='First')
        ProjectCheckpointFactory(project=project, name='Second')
        ProjectCheckpointFactory(project=project, name='Third')

        response = authenticated_client.get(f'/api/projects/{project.id}/checkpoints/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['name'] == 'Third'

    def test_list_checkpoints_project_not_found(self, authenticated_client, user):
        """Test listing checkpoints for non-existent project."""
        fake_id = uuid.uuid4()

        response = authenticated_client.get(f'/api/projects/{fake_id}/checkpoints/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_checkpoints_other_user(self, authenticated_client, user):
        """Test cannot list checkpoints of another user's project."""
        other_user = UserFactory()
        project = ProjectFactory(owner=other_user)

        response = authenticated_client.get(f'/api/projects/{project.id}/checkpoints/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_checkpoint_success(self, authenticated_client, user):
        """Test creating a checkpoint."""
        project = ProjectFactory(owner=user)

        data = {
            'name': 'Test Checkpoint',
            'description': 'Before major refactor'
        }

        response = authenticated_client.post(
            f'/api/projects/{project.id}/checkpoints/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Test Checkpoint'
        assert response.data['description'] == 'Before major refactor'
        assert response.data['is_auto'] is False

    def test_create_checkpoint_auto_name(self, authenticated_client, user):
        """Test checkpoint name is auto-generated if not provided."""
        project = ProjectFactory(owner=user)

        data = {}

        response = authenticated_client.post(
            f'/api/projects/{project.id}/checkpoints/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert 'Checkpoint' in response.data['name']

    def test_create_checkpoint_includes_snapshot(self, authenticated_client, user):
        """Test checkpoint includes state snapshot."""
        project = ProjectFactory(owner=user)

        data = {'name': 'Test'}

        response = authenticated_client.post(
            f'/api/projects/{project.id}/checkpoints/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        snapshot = response.data['state_snapshot']
        assert 'project_status' in snapshot
        assert 'manifest' in snapshot
        assert 'tasks_summary' in snapshot

    def test_create_checkpoint_project_not_found(self, authenticated_client, user):
        """Test creating checkpoint for non-existent project."""
        fake_id = uuid.uuid4()

        data = {'name': 'Test'}

        response = authenticated_client.post(
            f'/api/projects/{fake_id}/checkpoints/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_checkpoint_other_user(self, authenticated_client, user):
        """Test cannot create checkpoint for another user's project."""
        other_user = UserFactory()
        project = ProjectFactory(owner=other_user)

        data = {'name': 'Hacked'}

        response = authenticated_client.post(
            f'/api/projects/{project.id}/checkpoints/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
