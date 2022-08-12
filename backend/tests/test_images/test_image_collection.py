import pytest

from rest_framework import status


@pytest.fixture
def retrieve_collection_list(api_client):
    def do_retrieve_collection_list():
        return api_client.get('/images/')
    return do_retrieve_collection_list


@pytest.mark.django_db
class TestRetrivieCollectionList:
    def test_if_user_not_authenticate_returns_403(self, retrieve_collection_list):
        response = retrieve_collection_list()
        
        # 403 instead of 401 beacouse of session authentication
        assert response.status_code == status.HTTP_403_FORBIDDEN


    def test_if_not_data_returns_empty_list(
            self, 
            mute_signals, 
            create_user, 
            authenticate_user, 
            retrieve_collection_list
        ):
        
        user = create_user()
        authenticate_user(user)
        response = retrieve_collection_list()
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == []


    def test_if_user_authenticated_returns_200(
        self, 
        mute_signals, 
        create_user,
        create_collection,
        authenticate_user, 
        retrieve_collection_list
    ):
        user = create_user()
        authenticate_user(user)
        
        create_collection(user=user, quantity=2)
        create_collection()

        authenticate_user(user)
        response = retrieve_collection_list()
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2