from django.urls import path
from rest_framework import routers
from .views import UrlShortenerViewSet, DeleteUrlView ,redirect_view

router = routers.DefaultRouter()
router.register("api", UrlShortenerViewSet)


urlpatterns = [
    *router.urls,
    path("<str:short_code>/", redirect_view),
    path('api/delete', DeleteUrlView.as_view())
]
