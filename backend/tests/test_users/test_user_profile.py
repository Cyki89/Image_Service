import pytest

from rest_framework import status


@pytest.fixture
def get_user_profile(api_client):
    def do_get_user_profile(pk):
        return api_client.get(f'/auth/profile/{pk}/')
    return do_get_user_profile


@pytest.fixture
def update_user_profile(api_client):
    def do_update_user_profile(pk, data):
        return api_client.put(f'/auth/profile/{pk}/', data)
    return do_update_user_profile


@pytest.mark.django_db
class TestGetUserProfile:
    def test_if_wrong_pk_returns_404(self, get_user_profile):
        response = get_user_profile(0)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_correct_pk_returns_200(self, mute_signals, create_user, get_user_profile):
        user = create_user()
        response = get_user_profile(user.id)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username
        assert response.data['first_name'] == user.first_name
        assert response.data['last_name'] == user.last_name
        assert response.data['email'] == user.email


@pytest.mark.django_db
class TestUpdateUserProfile:
    def test_if_incorrect_data_returns_400(self, create_user, authenticate_user, update_user_profile, cleanup_user_folder):
        user1 = create_user(username="test")
        user1.email = "test@user.pl"
        user1.save()
        
        user2 = create_user(id=2, username="test2")
        authenticate_user(user2)
        
        data = {
            "username": "test", # existing username
            "first_name": "test",
            "last_name": "test",
            "email": "test@user.pl", # existing email
        }

        response = update_user_profile(user2.id, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data
        assert 'email' in response.data

        cleanup_user_folder()


    def test_if_correct_data_returns_200(self, create_user, authenticate_user, update_user_profile, cleanup_user_folder):
        user = create_user(username="test")
        authenticate_user(user)
        
        data = {
            "username": "test2",
            "first_name": "test",
            "last_name": "test",
            "email": "test@user.pl", 
        }
        
        response = update_user_profile(user.id, data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user.id
        assert response.data['username'] == data['username']
        assert response.data['account_type'] == user.account.tier.name
        assert response.data['allow_download'] == user.account.tier.allow_download

        cleanup_user_folder()