import pytest

from rest_framework.serializers import ValidationError
from images.models import Image, ImageCollection

from images.serializers import UploadImageSerializer


@pytest.mark.django_db
class TestUploadImageSerializers:
    def test_validate_name(
        self, 
        mute_signals, 
        create_user, 
        create_collection, 
        attach_user_to_serializer
    ):

        user = create_user()
        serializer = UploadImageSerializer()
        attach_user_to_serializer(serializer, user)

        name = 'test'
        
        # name is available
        validated_name = serializer.validate_name(name)
        assert name == validated_name

        # name is not available
        create_collection(user=user, name=name)
        with pytest.raises(ValidationError):
            validated_name = serializer.validate_name(name)

    def test_create_new_collection(
        self, 
        mute_signals, 
        create_user
    ):
        assert ImageCollection.objects.all().count() == 0

        user = create_user()
        name = 'test'

        serializer = UploadImageSerializer()
        collection = serializer._create_new_collection(name, user)

        assert ImageCollection.objects.all().count() == 1
        assert collection.name == name
        assert collection.user == user

    def test_save_orginal_image(
        self,
        create_user, 
        create_collection,
        create_account_tier,
        create_in_memo_image,
        cleanup_user_folder
    ):
        try:
            assert Image.objects.all().count() == 0
            
            user = create_user()
            name = 'test'
            collection = create_collection(name=name, user=user)
            
            serializer = UploadImageSerializer()
            in_memo_image = create_in_memo_image

            # invalid credentials
            basic_account = create_account_tier("Basic", False, False, [])
            image = serializer._save_orginal_image_if_allowed(in_memo_image, collection, basic_account) 
            
            assert image is None
            assert Image.objects.all().count() == 0

            # valid credentials
            enterprice_account = create_account_tier("Enterprice", True, True, [])
            image = serializer._save_orginal_image_if_allowed(in_memo_image, collection, enterprice_account)

            assert image is not None
            assert Image.objects.all().count() == 1
        finally:
            cleanup_user_folder()

    def test_get_image_types(self, create_in_memo_image):
        serializer = UploadImageSerializer()
        in_memo_image = create_in_memo_image
        
        # default content_type = 'image/png'
        django_type, pil_type = serializer._get_image_types_or_type_error(in_memo_image)
        assert django_type == 'image/png'
        assert pil_type == 'png'

        # change content_type to 'image/jpeg'
        in_memo_image.content_type = 'image/jpeg'
        django_type, pil_type = serializer._get_image_types_or_type_error(in_memo_image)
        assert django_type == 'image/jpeg'
        assert pil_type == 'jpeg'

        # change content_type to invalid value
        in_memo_image.content_type = 'invalid'
        with pytest.raises(TypeError):
            django_type, pil_type = serializer._get_image_types_or_type_error(in_memo_image)

    def test_create_thumbnail(self, create_in_memo_image, create_thumbnail):
        serializer = UploadImageSerializer()
        in_memo_image = create_in_memo_image
        thumbnail = create_thumbnail(200)
    
        in_memo_thubmnail = serializer._create_thumbnail(
            thumbnail, 
            in_memo_image, 
            'png', 
            'image/png', 
            'test', 
            'png'
        )

        assert in_memo_thubmnail.name == 'test_200.png'
        assert in_memo_thubmnail.content_type == 'image/png'

    def test_create_thumbnails(
        self,
        create_user,
        create_collection,
        create_thumbnail,
        create_account_tier,
        create_in_memo_image,
        cleanup_user_folder

    ):
        try:
            assert Image.objects.all().count() == 0

            thumb_200 = create_thumbnail(200)
            thumb_400 = create_thumbnail(400)
            basic_account = create_account_tier("Basic", False, False, [thumb_200, thumb_400])
            
            name = 'test'
            user = create_user(account_tier=basic_account)
            collection = create_collection(name=name, user=user)

            in_memo_image = create_in_memo_image

            serializer = UploadImageSerializer()
            thumbnails = serializer._create_thumbnails(in_memo_image, collection, basic_account)
            
            assert Image.objects.all().count() == 2
            assert len(thumbnails) == 2
            assert thumbnails[0].reduced_height == 200
            assert thumbnails[1].reduced_height == 400
        finally:
            cleanup_user_folder()
