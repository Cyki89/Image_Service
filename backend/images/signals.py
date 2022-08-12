import os
import shutil

from django.conf import settings
from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Account, ImageCollection, Image, DownloadUrl
from . import utils 
from extrernal_service import url_service


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_filedir(sender, instance, created, **kwargs):
    if created:
        os.mkdir(settings.MEDIA_ROOT / str(instance.id))


@receiver(post_delete, sender=User)
def delete_user_filedir(sender, instance, **kwargs):
    shutil.rmtree(settings.MEDIA_ROOT / str(instance.id))


@receiver(post_save, sender=ImageCollection)
def create_collection_filedir(sender, instance, created, **kwargs):
    if created:
        os.mkdir(settings.MEDIA_ROOT / str(instance.user_id) / str(instance.id))


@receiver(post_delete, sender=ImageCollection)
def delete_collection_filedir(sender, instance, **kwargs):
    shutil.rmtree(settings.MEDIA_ROOT / str(instance.user_id) / str(instance.id))


@receiver(pre_save, sender=Image)
def set_image_short_ur(sender, instance, **kwargs):
    if not instance.pk:
        url_obj = url_service.get_short_url(utils.get_image_link(instance.uuid))
        instance.short_url = url_obj['short_url']


@receiver(post_delete, sender=Image)
def delete_image_short_url_obj(sender, instance, **kwargs):
    url_service.delete_url_obj(utils.get_image_link(instance.uuid))


@receiver(post_delete, sender=DownloadUrl)
def delete_link_short_url_obj(sender, instance, **kwargs):
    url_service.delete_url_obj(utils.get_download_link(instance.url_hash))


@receiver(post_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    os.remove(instance.image.path)

