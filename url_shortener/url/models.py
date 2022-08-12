from django.db import models
from django.conf import settings


class UrlShortener(models.Model):
    full_url = models.URLField()
    short_code = models.CharField(max_length=settings.SHORT_CODE_LENGTH)