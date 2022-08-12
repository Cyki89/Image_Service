from django.contrib import admin
from .models import Account, AccountTier, ImageThumbnailType, Image, ImageCollection, DownloadUrl


admin.site.register(
    (Account, AccountTier, ImageThumbnailType, Image, ImageCollection, DownloadUrl)
)