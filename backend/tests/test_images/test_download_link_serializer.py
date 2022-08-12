import pytest
from datetime import timedelta

from django.utils import timezone
from rest_framework.serializers import ValidationError

from images.serializers import DownloadLinkSerializer
from images.models import DownloadUrl

@pytest.mark.django_db
class TestDowloadLinkSerializer:
    def test_validate_expire_time(self):
        serializer = DownloadLinkSerializer()
        min_val, max_val = 300, 30000
        expire_time = (min_val + max_val) // 2
        validated_expire_time = serializer.validate_expire_time(expire_time)
        assert expire_time == validated_expire_time
        
        expire_time = min_val - 1
        with pytest.raises(ValidationError):
            validated_expire_time = serializer.validate_expire_time(expire_time)

        expire_time = max_val + 1
        with pytest.raises(ValidationError):
            validated_expire_time = serializer.validate_expire_time(expire_time)

    def test_create(
        self, 
        create_collection,
        create_fake_image,
        create_image_object,
        create_user,
        attach_user_to_serializer,
        cleanup_user_folder
    ):
        try:
            assert DownloadUrl.objects.all().count() == 0
            
            user = create_user()
            serializer = DownloadLinkSerializer()
            attach_user_to_serializer(serializer, user)

            image_file = create_fake_image
            collection = create_collection(user=user)
            image_obj = create_image_object({"image": image_file, "collection": collection, "is_orginal": True})

            expire_time = 3000
            url_obj, _ = serializer.create({"image_id": image_obj.id, "expire_time": expire_time})
            
            assert DownloadUrl.objects.all().count() == 1
            assert (timezone.now() + timedelta(seconds=expire_time)) - url_obj.expire_time < timedelta(seconds=10)

        
        finally:
            cleanup_user_folder()