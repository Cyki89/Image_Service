import os
import shutil

import pytest
from model_bakery import baker

from django.conf import settings as django_settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.test import APIClient

from images.models import ImageCollection
from images.signals import create_user_filedir, create_collection_filedir


@pytest.fixture(autouse=True)
def use_test_media_root(settings):
    settings.MEDIA_ROOT=settings.TEST_MEDIA_ROOT


@pytest.fixture()
def user_media_folder(settings):
    def get_user_media_folder(id=1):
        return django_settings.TEST_MEDIA_ROOT / str(id)
    return get_user_media_folder


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def mute_signals(request):
    post_save.disconnect(create_user_filedir, sender=User)
    post_save.disconnect(create_collection_filedir, sender=ImageCollection)


@pytest.fixture
def unmute_signals(request):
    post_save.connect(create_user_filedir, sender=User)
    post_save.connect(create_collection_filedir, sender=ImageCollection)


@pytest.fixture
def create_user(api_client):
    def do_create_user(
        id=1,
        username='test', 
        password='test_1234', 
        account_tier=None
    ):
        user = baker.make(User, username=username, id=id)       
        user.set_password(password)
        user.save()

        if account_tier:
            account = user.account
            account.tier = account_tier
            account.save()
        
        return user
    
    return do_create_user


@pytest.fixture
def authenticate_user(api_client):
    def do_authenticate(user):
        return api_client.force_login(user)
    
    return do_authenticate


@pytest.fixture
def cleanup_user_folder():
    def do_cleanup_user_folder(id=1):
        user_folder = django_settings.TEST_MEDIA_ROOT / str(id)
        if os.path.exists(user_folder):
            shutil.rmtree(user_folder)
    
    return do_cleanup_user_folder