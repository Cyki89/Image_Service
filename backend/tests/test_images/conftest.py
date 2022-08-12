import io
import sys

import pytest
from pytest_mock import mocker
from model_bakery import baker
from PIL import Image as PilImage

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from images.models import AccountTier, Image, ImageCollection, ImageThumbnailType
from extrernal_service.url_service import BASE_URL


TEST_URL_OBJ = {
    'id': 1,
    'short_code' : 'short',
    'short_url': BASE_URL + 'short',
    'full_url': BASE_URL + 'full',
}


@pytest.fixture(autouse=True)
def mute_url_service(request, mocker):
    mocker.patch(
        'extrernal_service.url_service.get_short_url', return_value=TEST_URL_OBJ
    )

@pytest.fixture
def create_thumbnail(api_client):
    def do_create_thumbnail(height):
        thumbnail = baker.make(ImageThumbnailType, height=height)
        
        return thumbnail

    return do_create_thumbnail


@pytest.fixture
def create_account_tier(api_client):
    def do_create_account_tier(name, allow_orginal, allow_download, thumbnails):
        account_tier = baker.make(
            AccountTier, 
            name=name, 
            allow_orginal=allow_orginal, 
            allow_download=allow_download
        )

        for thumbnail in thumbnails:
            account_tier.thumbnails.add(thumbnail)

        return account_tier

    return do_create_account_tier


@pytest.fixture
def create_fake_image(api_client):
    image_file = io.BytesIO()
    
    image = PilImage.new("RGBA", size=(800, 800))
    image.save(image_file, 'png')
    
    image_file.name = 'test.png'
    image_file.content_type = 'image/png'
    image_file._committed = True # for testing purpose
    image_file.seek(0)

    return image_file


@pytest.fixture
def create_in_memo_image(api_client, create_fake_image):
    fake_image = create_fake_image 
    
    return InMemoryUploadedFile(
        file=fake_image,
        field_name='ImageField',
        name=fake_image.name,
        content_type=fake_image.content_type,
        size=sys.getsizeof(fake_image), 
        charset=None
    )


@pytest.fixture
def create_image_object(api_client):
    def do_create_image_object(data):
        image = baker.make(Image, **data)
        return image
    
    return do_create_image_object


@pytest.fixture
def create_collection(api_client):
    def do_create_collection(user=None, quantity=None, name=None):
        data = {}
        if user:
            data['user'] = user 
        if quantity:
            data['_quantity'] = quantity
        if name:
            data['name'] = name
        
        collection = baker.make(ImageCollection, **data)
        
        return collection

    return do_create_collection


@pytest.fixture
def attach_user_to_serializer(api_client):
    def do_attach_user_to_serializer(serializer, user):
        class Object(object): 
            ...
        
        serializer.context['request'] = Object()
        serializer.context['request'].user = user

    return do_attach_user_to_serializer