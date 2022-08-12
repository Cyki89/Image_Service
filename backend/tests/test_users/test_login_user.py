import pytest

from rest_framework import status
from django.contrib.auth.models import User


@pytest.fixture
def login_user(api_client):
    def do_login_user(data):
        return api_client.post('/auth/login/', data)
    return do_login_user


@pytest.mark.django_db
class TestLoginUser:
    def test_no_data_returns_400(self, login_user):
        data = {
            "username": "",
            "password": "",
        }
        
        response = login_user(data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data
        assert 'password' in response.data

    def test_if_invalid_credentials_returns_400(self, mute_signals, create_user, login_user):
        create_user(username='test', password='test_1234')
        assert User.objects.all().count() == 1
        
        data = {
            "username": "test",
            "password": "test",
        }  
        response = login_user(data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data
    
    def test_if_valid_credentials_returns_200(self, create_user, login_user, cleanup_user_folder):
        user = create_user(username='test', password='test_1234')
        assert User.objects.all().count() == 1

        data = {
            "username": "test",
            "password": "test_1234",
        }
        response = login_user(data)
        assert response.status_code == status.HTTP_200_OK
        assert user.id == response.data['id']
        assert 'sessionid' in response.cookies
        
        cleanup_user_folder()