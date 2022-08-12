import pytest

from rest_framework import status
from images.models import DownloadUrl


@pytest.fixture
def retrieve_download_link(api_client):
    def do_retrieve_download_link(data):
        return api_client.post('/images/download', data)
    return do_retrieve_download_link


@pytest.mark.django_db
class TestRetrivieDownloadLink:
    def test_if_user_not_authenticate_returns_403(self, retrieve_download_link):
        response = retrieve_download_link({})
        
        # 403 instead of 401 beacouse of session authentication
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_invalid_credetnials_returns_403(
        self, mute_signals, create_user, authenticate_user, retrieve_download_link
    ):
        user = create_user()
        authenticate_user(user)

        response = retrieve_download_link({})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_invalid_image_id_returns_400(
        self, mute_signals, create_user, authenticate_user, create_account_tier, retrieve_download_link
    ):
        account_tier = create_account_tier("Enterprice", True, True, [])
        user = create_user(account_tier=account_tier)
        authenticate_user(user)

        response = retrieve_download_link({})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_valid_data_return_201(
        self, 
        create_account_tier,
        create_collection,
        create_fake_image,
        create_image_object,
        create_user,
        authenticate_user, 
        retrieve_download_link,
        cleanup_user_folder

    ):
        try:
            account_tier = create_account_tier("Enterprice", True, True, [])
            user = create_user(account_tier=account_tier)
            authenticate_user(user)

            image_file = create_fake_image
            collection = create_collection(user=user)
            image = create_image_object({"image": image_file, "collection": collection, "is_orginal": True})

            response = retrieve_download_link({"image_id": image.id, "expire_time": 3000})
            link = response.data['download_link']
            url_obj = DownloadUrl.objects.first() 
            
            # assert url_obj.short_url == link
            assert response.status_code == status.HTTP_201_CREATED
        finally:
            cleanup_user_folder()