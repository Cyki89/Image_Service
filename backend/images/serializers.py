import sys
from io import BytesIO
from datetime import timedelta
from uuid import uuid1
from PIL import Image as PILImage

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import server_error

from . import utils
from .models import Image, ImageCollection, DownloadUrl

from extrernal_service import url_service


class UploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    name = serializers.CharField(max_length=255)

    def validate_name(self, name):
        user = self.context['request'].user
        if ImageCollection.objects.filter(name=name, user_id=user.id).exists():
            raise serializers.ValidationError('Name is not available.')
        
        return name

    def create(self, validated_data):
        collection_name = validated_data['name']
        in_memo_image = validated_data['image']
        
        user = self.context['request'].user
        account_tier = user.account.tier
        
        collection = self._create_new_collection(collection_name, user)

        orginal = self._save_orginal_image_if_allowed(in_memo_image, collection, account_tier)

        thumbnails = self._create_thumbnails(in_memo_image, collection, account_tier)
        
        response = self._create_response(collection, orginal, thumbnails)

        return response

    def _create_new_collection(self, name, user):
        collection = ImageCollection(name=name, user=user)
        collection.save()
        
        return collection

    def _save_orginal_image_if_allowed(self, in_memo_image, collection, account_tier):
        if not account_tier.allow_orginal:
            return 
        
        return Image.objects.create(
            image=in_memo_image, 
            collection=collection, 
            is_orginal=True)

    def _create_thumbnails(self, in_memo_image, collection, account_tier):
        thumbnails = account_tier.thumbnails.all()
        if not thumbnails:
            return

        django_type, pill_type = self._get_image_types_or_type_error(in_memo_image)
        image_name, image_ext = in_memo_image.name.split('.')
        
        thumbnail_objs = []
        for thumbnail in thumbnails:
            in_memo_thubmnail = self._create_thumbnail(
                thumbnail, 
                in_memo_image, 
                pill_type, 
                django_type, 
                image_name, 
                image_ext
            )
            
            thumbnail_objs.append(Image.objects.create(
                image=in_memo_thubmnail, 
                reduced_height=thumbnail.height,
                collection=collection,
            ))

        return thumbnail_objs

    def _get_image_types_or_type_error(self, image):
        django_type = image.content_type
        if django_type == 'image/jpeg':
            pil_type = 'jpeg'
        elif django_type == 'image/png':
            pil_type = 'png'
        else:
            raise TypeError('Invalid file type!')

        return django_type, pil_type

    def _create_thumbnail(self, thumbnail, in_memo_image, pill_type, 
                          django_type, image_name, image_ext):
        output = BytesIO()
        
        pill_image = PILImage.open(in_memo_image)
        pill_image.thumbnail((pill_image.width, thumbnail.height))
        pill_image.save(output, format=pill_type)
        
        thumbnail_name = f'{image_name}_{thumbnail.height}.{image_ext}'
        in_memo_thubmnail = InMemoryUploadedFile(
            file=output,
            field_name='ImageField',
            name=thumbnail_name,
            content_type=django_type,
            size=sys.getsizeof(output), 
            charset=None
        )
        
        return in_memo_thubmnail

    def _create_response(self, collection, orginal, thumbnails):
        response = {"name" : collection.name}
        if orginal:
            response['orginal'] = orginal.short_url
        if thumbnails:
            response['thumbnails'] =  [
                {
                    f'thumbnail {thumbnail.reduced_height}px': thumbnail.short_url
                } for thumbnail in thumbnails
            ]

        return response

    def to_representation(self, instance):
        return instance


class UploadedImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageCollection
        fields = ["id", "name", "orginal", "thumbnails"]
    
    orginal = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()

    def get_orginal(self, collection):
        if orginal := collection.orginal():
            return {
                "id": orginal.id,
                "name": utils.get_image_name(orginal.image.name),
                "link": orginal.short_url
            }

    def get_thumbnails(self, collection):
       if thumbnails := collection.thumbnails():
            return [
                {   "id": thumbnail.id,
                    "name": utils.get_image_name(thumbnail.image.name),
                    "height": thumbnail.reduced_height,
                    "link": thumbnail.short_url
                } for thumbnail in thumbnails
            ] 


class DownloadLinkSerializer(serializers.Serializer):
    image_id = serializers.IntegerField()
    expire_time = serializers.IntegerField()

    def validate_expire_time(self, expire_time):
        min_val, max_val = 300, 30000
        if not min_val <= expire_time <= max_val:
            raise serializers.ValidationError("Expire time must be between 300 and 30000 seconds")
        
        return expire_time

    def create(self, validated_data):
        user = self.context['request'].user
        image_id = validated_data['image_id']
        image_obj = get_object_or_404(Image, id=image_id, collection__user_id=user.id)
        
        with transaction.atomic():
            expire_time = validated_data['expire_time'] 
            url_obj =  DownloadUrl.objects.create(
                image_path  = image_obj.image.path,
                expire_time = timezone.now() + timedelta(seconds=expire_time)
            )

            download_link = utils.get_download_link(url_obj.url_hash)
            short_url = url_service.get_short_url(download_link)
            if not short_url:
                raise Exception("External Api Failed")
            return url_obj, short_url

    def to_representation(self, instances):
        url_obj, short_url = instances
        return {"download_link": short_url['short_url']}
