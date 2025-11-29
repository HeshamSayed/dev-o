"""
Unit tests for Project Create API endpoint.

POST /api/projects/
"""
import pytest
from rest_framework import status
from apps.projects.tests.factories import ProjectFactory
from apps.accounts.tests.factories import UserFactory, SubscriptionFactory


@pytest.mark.django_db
class TestProjectCreateAPI:
    """Tests for POST /api/projects/ endpoint."""

    def test_create_project_success(self, authenticated_client, user):
        """Test creating a project with valid data."""
        data = {
            'name': 'Test Project',
            'description': 'Test description'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Test Project'
        assert response.data['description'] == 'Test description'
        assert response.data['status'] == 'initializing'
        assert str(response.data['owner']) == str(user.id)

    def test_create_project_with_optional_fields(self, authenticated_client, user):
        """Test creating a project with optional fields."""
        data = {
            'name': 'Test Project',
            'description': 'Test description',
            'local_path': '/path/to/project',
            'repository_url': 'https://github.com/user/repo'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['local_path'] == '/path/to/project'
        assert response.data['repository_url'] == 'https://github.com/user/repo'

    def test_create_project_initializes_manifest(self, authenticated_client, user):
        """Test project creation initializes manifest."""
        data = {
            'name': 'Test Project',
            'description': 'Test description'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        manifest = response.data['manifest']
        assert 'name' in manifest
        assert 'tech_stack' in manifest
        assert 'architecture' in manifest

    def test_create_project_missing_name(self, authenticated_client, user):
        """Test creating project without name fails."""
        data = {
            'description': 'Test description'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data

    def test_create_project_missing_description(self, authenticated_client, user):
        """Test creating project without description fails."""
        data = {
            'name': 'Test Project'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'description' in response.data

    def test_create_project_duplicate_name(self, authenticated_client, user):
        """Test creating project with duplicate name fails."""
        ProjectFactory(owner=user, name='Existing Project')

        data = {
            'name': 'Existing Project',
            'description': 'Test description'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'name' in response.data

    def test_create_project_same_name_different_user(self, authenticated_client, user):
        """Test can create project with same name as another user."""
        other_user = UserFactory()
        ProjectFactory(owner=other_user, name='Same Name')

        data = {
            'name': 'Same Name',
            'description': 'Test description'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_project_subscription_limit(self, authenticated_client, user):
        """Test subscription project limit is enforced."""
        # Create subscription with limit of 2
        SubscriptionFactory(user=user, max_projects=2)

        # Create 2 projects
        ProjectFactory.create_batch(2, owner=user)

        # Try to create a third
        data = {
            'name': 'Third Project',
            'description': 'Test description'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert 'Maximum project limit' in response.data['error']

    def test_create_project_unlimited_subscription(self, authenticated_client, user):
        """Test unlimited subscription allows many projects."""
        # Create subscription with unlimited projects (-1)
        SubscriptionFactory(user=user, max_projects=-1)

        # Create many projects
        ProjectFactory.create_batch(10, owner=user)

        data = {
            'name': 'Another Project',
            'description': 'Test description'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_project_unauthenticated(self, api_client):
        """Test unauthenticated access is denied."""
        data = {
            'name': 'Test Project',
            'description': 'Test description'
        }

        response = api_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
