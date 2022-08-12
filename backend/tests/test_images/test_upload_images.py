import pytest

from rest_framework import status


@pytest.fixture
def upload_image(api_client):
    def upload_image(data):
        return api_client.post('/images/', data)
    return upload_image


@pytest.mark.django_db
class TestUploadImage:
    def test_if_user_not_authenticated_returns_403(self, upload_image):
        response = upload_image({})
        
        # 403 instead of 401 beacouse of session authentication
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_invalid_data_returns_400(
        self, 
        mute_signals,
        upload_image, 
        create_user, 
        authenticate_user,
    ):
        user = create_user()
        authenticate_user(user)
        
        data = {
            "name": "test",
            "image": ''
        }
        
        response = upload_image(data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'image' in response.data

    def test_if_valid_data_return_201(
        self,
        create_user,
        authenticate_user, 
        upload_image, 
        create_fake_image,
        cleanup_user_folder
    ):
        try:
            user = create_user()
            authenticate_user(user)
            
            data = {
                "name": "test",
                "image": create_fake_image
            }
            
            response = upload_image(data)
        
            assert response.data['name'] == 'test'
            assert 'thumbnails' in response.data
            assert not 'orginal' in response.data
            assert response.status_code == status.HTTP_201_CREATED
        
        finally:
            cleanup_user_folder()

    def test_if_enterprice_user_return_201(
        self,
        create_account_tier,
        create_user,
        authenticate_user, 
        upload_image, 
        create_fake_image,
        cleanup_user_folder
    ):
        try:
            account_tier = create_account_tier("Enterprice", True, True, [])
            user = create_user(account_tier=account_tier)
            authenticate_user(user)
            
            data = {
                "name": "test",
                "image": create_fake_image
            }
            response = upload_image(data)
        
            assert response.data['name'] == 'test'
            assert not 'thumbnails' in response.data
            assert 'orginal' in response.data
            assert response.status_code == status.HTTP_201_CREATED
        finally:
            cleanup_user_folder()