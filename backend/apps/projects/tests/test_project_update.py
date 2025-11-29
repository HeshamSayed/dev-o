"""
Unit tests for Project Update API endpoint.

PATCH /api/projects/{id}/
"""
import pytest
import uuid
from rest_framework import status
from apps.projects.tests.factories import ProjectFactory
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestProjectUpdateAPI:
    """Tests for PATCH /api/projects/{id}/ endpoint."""

    def test_update_project_name(self, authenticated_client, user):
        """Test updating project name."""
        project = ProjectFactory(owner=user, name='Original Name')

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

    def test_update_project_description(self, authenticated_client, user):
        """Test updating project description."""
        project = ProjectFactory(owner=user)

        data = {'description': 'Updated description'}
        response = authenticated_client.patch(
            f'/api/projects/{project.id}/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['description'] == 'Updated description'

    def test_update_project_status(self, authenticated_client, user):
        """Test updating project status."""
        project = ProjectFactory(owner=user, status='initializing')

        data = {'status': 'in_progress'}
        response = authenticated_client.patch(
            f'/api/projects/{project.id}/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'in_progress'

    def test_update_project_manifest(self, authenticated_client, user):
        """Test updating project manifest."""
        project = ProjectFactory(owner=user)

        new_manifest = {
            'tech_stack': {'backend': 'Django'},
            'requirements': {'functional': ['User auth']}
        }
        data = {'manifest': new_manifest}
        response = authenticated_client.patch(
            f'/api/projects/{project.id}/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['manifest']['tech_stack']['backend'] == 'Django'

    def test_update_project_partial(self, authenticated_client, user):
        """Test partial update only changes specified fields."""
        project = ProjectFactory(
            owner=user,
            name='Original',
            description='Original desc'
        )

        data = {'name': 'Updated'}
        response = authenticated_client.patch(
            f'/api/projects/{project.id}/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated'
        assert response.data['description'] == 'Original desc'

    def test_update_project_duplicate_name(self, authenticated_client, user):
        """Test updating to duplicate name fails."""
        ProjectFactory(owner=user, name='Existing')
        project = ProjectFactory(owner=user, name='Original')

        data = {'name': 'Existing'}
        response = authenticated_client.patch(
            f'/api/projects/{project.id}/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_project_same_name_allowed(self, authenticated_client, user):
        """Test updating with same name is allowed."""
        project = ProjectFactory(owner=user, name='Same Name')

        data = {'name': 'Same Name', 'description': 'New desc'}
        response = authenticated_client.patch(
            f'/api/projects/{project.id}/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK

    def test_update_project_not_found(self, authenticated_client, user):
        """Test updating non-existent project returns 404."""
        fake_id = uuid.uuid4()

        data = {'name': 'Updated'}
        response = authenticated_client.patch(
            f'/api/projects/{fake_id}/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_project_other_user(self, authenticated_client, user):
        """Test cannot update another user's project."""
        other_user = UserFactory()
        project = ProjectFactory(owner=other_user)

        data = {'name': 'Hacked'}
        response = authenticated_client.patch(
            f'/api/projects/{project.id}/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_project_unauthenticated(self, api_client, user):
        """Test unauthenticated access is denied."""
        project = ProjectFactory(owner=user)

        data = {'name': 'Updated'}
        response = api_client.patch(
            f'/api/projects/{project.id}/',
            data,
            format='json'
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
