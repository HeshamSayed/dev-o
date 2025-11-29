"""
Integration tests for projects API endpoints.
"""
import pytest
from rest_framework import status
from apps.projects.tests.factories import ProjectFactory, ProjectCheckpointFactory
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestProjectAPI:
    """Tests for Project API endpoints."""

    def test_list_projects(self, authenticated_client, user):
        """Test listing projects."""
        # Create test projects
        ProjectFactory.create_batch(3, owner=user)

        response = authenticated_client.get('/api/projects/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_project(self, authenticated_client, user):
        """Test creating a project."""
        data = {
            'name': 'Test Project',
            'description': 'Test description',
            'manifest': {}
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Test Project'
        assert response.data['owner'] == user.id

    def test_get_project(self, authenticated_client, user):
        """Test retrieving a project."""
        project = ProjectFactory(owner=user)

        response = authenticated_client.get(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == project.name

    def test_update_project(self, authenticated_client, user):
        """Test updating a project."""
        project = ProjectFactory(owner=user)

        data = {'name': 'Updated Name'}
        response = authenticated_client.patch(
            f'/api/projects/{project.id}/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Name'

        project.refresh_from_db()
        assert project.name == 'Updated Name'

    def test_delete_project(self, authenticated_client, user):
        """Test deleting a project."""
        project = ProjectFactory(owner=user)

        response = authenticated_client.delete(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify project was deleted
        from apps.projects.models import Project
        assert not Project.objects.filter(id=project.id).exists()

    def test_unauthorized_access(self, api_client, user):
        """Test that unauthenticated users cannot access projects."""
        project = ProjectFactory(owner=user)

        response = api_client.get(f'/api/projects/{project.id}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_access_other_users_project(self, authenticated_client, user):
        """Test that users cannot access other users' projects."""
        other_user = UserFactory()
        project = ProjectFactory(owner=other_user)

        response = authenticated_client.get(f'/api/projects/{project.id}/')

        # Should return 404 (not 403) to avoid information leakage
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestProjectStatusAPI:
    """Tests for project status endpoint."""

    def test_get_project_status(self, authenticated_client, user):
        """Test getting project status."""
        project = ProjectFactory(owner=user, status='in_progress')

        response = authenticated_client.get(f'/api/projects/{project.id}/status/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'in_progress'


@pytest.mark.django_db
class TestProjectCheckpointAPI:
    """Tests for project checkpoint endpoints."""

    def test_list_checkpoints(self, authenticated_client, user):
        """Test listing project checkpoints."""
        project = ProjectFactory(owner=user)
        ProjectCheckpointFactory.create_batch(3, project=project)

        response = authenticated_client.get(f'/api/projects/{project.id}/checkpoints/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_create_checkpoint(self, authenticated_client, user):
        """Test creating a checkpoint."""
        project = ProjectFactory(owner=user)

        data = {
            'name': 'Test Checkpoint',
            'description': 'Test checkpoint description'
        }

        response = authenticated_client.post(
            f'/api/projects/{project.id}/checkpoints/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Test Checkpoint'
