import pytest

from rest_framework import status


@pytest.fixture
def get_csrf(api_client):
    def do_get_csrf():
        return api_client.get(f'/auth/csrf/')
    return do_get_csrf


@pytest.fixture
def get_auth_user(api_client):
    def do_get_auth_user():
        return api_client.get('/auth/authentication/')
    return do_get_auth_user


@pytest.mark.django_db
class TestAuthentication:
    def test_if_csrf_is_set(self, get_csrf):
        response = get_csrf()
        
        assert response.status_code == status.HTTP_200_OK
        assert 'csrftoken' in response.cookies

    def test_if_no_auth_user_returns_401(self, get_auth_user, cleanup_user_folder):
        response = get_auth_user()
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_auth_user_returns_200(self, create_user, authenticate_user, get_auth_user, cleanup_user_folder):
        user = create_user()
        authenticate_user(user)
        response = get_auth_user()
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user.id
        assert response.data['username'] == user.username
        assert response.data['account_type'] == user.account.tier.name
        assert response.data['allow_download'] == user.account.tier.allow_download
        
        cleanup_user_folder()