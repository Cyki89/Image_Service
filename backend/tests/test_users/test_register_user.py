import pytest
import os

from rest_framework import status
from django.contrib.auth.models import User
from images.models import Account


@pytest.fixture
def register_user(api_client):
    def do_register_user(data):
        return api_client.post('/auth/register/', data)
    return do_register_user


@pytest.mark.django_db
class TestRegisterUser:
    def test_no_data_returns_400(self, register_user):
        data = {
            "username": "",
            "password": "",
            "confirm_password": ""
        }
        
        response = register_user(data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert User.objects.all().count() == 0
        assert 'username' in response.data
        assert 'password' in response.data
        assert 'confirm_password' in response.data

    def test_if_invalid_password_returns_400(self, register_user):
        data = {
            "username": "test",
            "password": "test",
            "confirm_password": "test"
        }
        
        response = register_user(data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert User.objects.all().count() == 0
        assert 'password' in response.data
    
    def test_if_diffrent_password_returns_400(self, register_user):
        data = {
            "username": "test",
            "password": "test_1234",
            "confirm_password": "test_1235"
        }
        
        response = register_user(data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert User.objects.all().count() == 0
        assert 'password' in response.data
        assert 'confirm_password' in response.data

    def test_if_valid_data_returs_201(self, unmute_signals, register_user, user_media_folder, cleanup_user_folder):
        data = {
            "username": "test",
            "password": "test_1234",
            "confirm_password": "test_1234"
        }
        
        response = register_user(data)
        assert data['username'] == response.data['username']
        assert 'sessionid' in response.cookies
        assert response.status_code == status.HTTP_200_OK
        assert User.objects.all().count() == 1
        assert Account.objects.all().count() == 1
        assert os.path.exists(user_media_folder(id=response.data['id']))

        cleanup_user_folder(id=response.data['id'])

    def test_if_username_exists_returns_400(
        self,
        mute_signals,
        create_user,
        register_user, 
    ):
        create_user()
        assert User.objects.all().count() == 1

        data = {
            "username": "test",
            "password": "test_1234",
            "confirm_password": "test_1234"
        }
        
        response = register_user(data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data
        assert User.objects.all().count() == 1