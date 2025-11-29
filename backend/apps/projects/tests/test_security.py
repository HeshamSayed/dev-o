"""
Security and edge case tests for Project API.
"""
import pytest
from rest_framework import status
from apps.projects.tests.factories import ProjectFactory


@pytest.mark.django_db
class TestProjectAPISecurity:
    """Security and edge case tests for Project API."""

    def test_invalid_uuid_returns_404(self, authenticated_client, user):
        """Test invalid UUID in path returns 404."""
        response = authenticated_client.get('/api/projects/not-a-uuid/')

        # Django returns 404 for invalid UUID format
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_sql_injection_attempt(self, authenticated_client, user):
        """Test SQL injection is prevented."""
        data = {
            'name': "'; DROP TABLE projects; --",
            'description': 'Test'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        # Should either create safely or reject
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST
        ]

    def test_xss_attempt_in_name(self, authenticated_client, user):
        """Test XSS attempt is stored safely."""
        data = {
            'name': '<script>alert("xss")</script>',
            'description': 'Test'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        # Content should be stored as-is (escaped on frontend)
        assert '<script>' in response.data['name']

    def test_very_long_name_rejected(self, authenticated_client, user):
        """Test very long name is rejected."""
        data = {
            'name': 'x' * 500,  # Exceeds max_length=255
            'description': 'Test'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_body_post(self, authenticated_client, user):
        """Test POST with empty body fails validation."""
        response = authenticated_client.post('/api/projects/', {}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_json_content_type_required(self, authenticated_client, user):
        """Test content type handling."""
        data = {
            'name': 'Test',
            'description': 'Test'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_method_not_allowed_put(self, authenticated_client, user):
        """Test PUT method is not allowed on detail endpoint."""
        project = ProjectFactory(owner=user)

        data = {'name': 'Updated', 'description': 'Updated'}
        response = authenticated_client.put(
            f'/api/projects/{project.id}/',
            data,
            format='json'
        )

        # PUT should not be allowed (only PATCH)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_method_not_allowed_patch_on_list(self, authenticated_client, user):
        """Test PATCH method is not allowed on list endpoint."""
        data = {'name': 'Updated'}
        response = authenticated_client.patch('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_unicode_in_project_name(self, authenticated_client, user):
        """Test unicode characters in project name."""
        data = {
            'name': '项目名称 🚀 مشروع',
            'description': 'Test unicode'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == '项目名称 🚀 مشروع'

    def test_null_values_rejected(self, authenticated_client, user):
        """Test null values are rejected for required fields."""
        data = {
            'name': None,
            'description': 'Test'
        }

        response = authenticated_client.post('/api/projects/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
