from django.shortcuts import get_object_or_404, redirect
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin
from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.viewsets import GenericViewSet
from .models import UrlShortener
from .serializers import UrlShortenerSerializer


def redirect_view(request, short_code):
    url_model = get_object_or_404(UrlShortener, short_code=short_code)
    return redirect(url_model.full_url)


class UrlShortenerViewSet(RetrieveModelMixin, CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = UrlShortener.objects.all()
    serializer_class = UrlShortenerSerializer
    lookup_field = 'short_code'


class DeleteUrlView(APIView):
    def post(self, request, *args, **kwargs):
        [obj_deleted, _] = UrlShortener.objects.filter(full_url=request.POST['full_url']).delete()
        if obj_deleted == 0:
            return Response({'Detail' : 'Url object not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)
        