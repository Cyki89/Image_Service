from django.urls import path
from .views import UploadedImagesView, DownloadLinkView, download_view, image_view 


urlpatterns = [
    path("", UploadedImagesView.as_view()),
    path("download", DownloadLinkView.as_view()),
    path("download/<str:url_hash>", download_view),
    path("<str:uuid>", image_view)
]