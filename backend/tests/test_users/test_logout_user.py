import pytest

from rest_framework import status
from django.contrib.auth.models import User


@pytest.fixture
def logout_user(api_client):
    def do_logout_user():
        return api_client.get('/auth/logout/')
    return do_logout_user


@pytest.mark.django_db
class TestLogoutUser:
    def test_if_no_user_returns_401(self, logout_user):
        response = logout_user()
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_user_return_200(
        self,
        mute_signals,
        create_user, 
        authenticate_user, 
        logout_user, 
    ):
        user = create_user(username='test', password='test_1234')
        assert User.objects.all().count() == 1
        
        authenticate_user(user)
        response = logout_user()

        assert response.status_code == status.HTTP_200_OK