from celery import shared_task
from django.utils import timezone

from django.core import management
from . import models

@shared_task
def cleanup():
    """Cleanup expired sessions by using Django management command."""
    print('cleanup sessions')
    management.call_command("clearsessions", verbosity=0)


@shared_task
def delete_expire_links():
    """Cleanup expired links"""
    print('delete expire links')
    models.DownloadUrl.objects.filter(expire_time__lt = timezone.now()).delete()