from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http.response import Http404, FileResponse

from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework import permissions, parsers

from . import permissions as custom_permissions 
from . import utils
from .models import Image, ImageCollection, DownloadUrl
from .serializers import UploadImageSerializer, UploadedImageListSerializer, DownloadLinkSerializer
from extrernal_service import url_service


class UploadedImagesView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    serializer_class = UploadImageSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UploadImageSerializer
        return UploadedImageListSerializer

    def get_queryset(self):
        return ImageCollection.objects.filter(user_id=self.request.user.id).order_by("-id")


class DownloadLinkView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, custom_permissions.DownloadLinkAllowed]
    serializer_class = DownloadLinkSerializer


def image_view(request, uuid):
    image_obj = get_object_or_404(Image,  uuid = uuid)
    return FileResponse(open(image_obj.image.path, 'rb'), as_attachment=False)


def download_view(request, url_hash):
    url_obj = get_object_or_404(DownloadUrl, url_hash=url_hash)
    if url_obj.expire_time < timezone.now():
        url_obj.delete()
        raise Http404("Link is not longer available")
    try:
        return FileResponse(open(url_obj.image_path, 'rb'), as_attachment=True)
    except [FileNotFoundError, AssertionError]:
        url_obj.delete()
        raise Http404("Link is not longer available")