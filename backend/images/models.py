from uuid import uuid1
from django.db import models
from django.contrib.auth.models import User


class ImageCollection(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='collections', on_delete=models.CASCADE)

    def orginal(self):
        return self.images.filter(is_orginal=True).first()
    
    def thumbnails(self):
        return self.images.filter(is_orginal=False)

    def thumbnail(self, height):
        return self.images.filter(reduced_height=height).first()

    class Meta:
        unique_together = ('name', 'user')


def get_upload_path(instance, filename):
    user_id = instance.collection.user_id
    collection_id = instance.collection_id
    return f'{user_id}/{collection_id}/{filename}'


class Image(models.Model):
    uuid = models.UUIDField(default=uuid1)
    image = models.ImageField(upload_to=get_upload_path)
    short_url=models.URLField(null=True)
    is_orginal = models.BooleanField(default=False)
    reduced_height = models.IntegerField(null=True, blank=True)
    collection = models.ForeignKey(ImageCollection, related_name='images', on_delete=models.CASCADE)


class ImageThumbnailType(models.Model):
    height = models.IntegerField()

    @staticmethod
    def sentinel_thumbnail():
        return ImageThumbnailType.objects.get_or_create(height=200)[0]

    @staticmethod
    def sentinel_thumbnail_id():
        return ImageThumbnailType.sentinel_thumbnail().id

    def __str__(self):
        return f'{self.height}px'


class AccountTier(models.Model):
    name = models.CharField(max_length=255)
    thumbnails = models.ManyToManyField(ImageThumbnailType)
    allow_orginal = models.BooleanField(default=False)
    allow_download = models.BooleanField(default=False)

    @staticmethod
    def sentinel_account_tier():
        account_tier, created = AccountTier.objects.get_or_create(name="Basic")
        if created:
            account_tier.thumbnails.add(ImageThumbnailType.sentinel_thumbnail_id())
            account_tier.save()
        
        return account_tier

    @staticmethod   
    def sentinel_account_tier_id():
        return AccountTier.sentinel_account_tier().id

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(
        AccountTier, 
        on_delete=models.SET(AccountTier.sentinel_account_tier), 
        default=AccountTier.sentinel_account_tier_id
    )

    def __str__(self):
        return self.user.username


class DownloadUrl(models.Model):
    image_path = models.CharField(max_length=255)
    url_hash = models.UUIDField(default=uuid1)
    expire_time = models.DateTimeField()