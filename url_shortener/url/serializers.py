from django.conf import settings
from rest_framework import serializers
from .utils import generate_new_short_code
from .models import UrlShortener


class UrlShortenerSerializer(serializers.ModelSerializer):
    short_code = serializers.CharField(max_length=settings.SHORT_CODE_LENGTH, read_only=True)

    class Meta:
        model = UrlShortener
        fields = ['id', 'full_url', 'short_code']

    def save(self, **kwargs):
        full_url = self.validated_data['full_url']

        if UrlShortener.objects.filter(full_url=full_url).exists():
            self.instance = UrlShortener.objects.get(full_url=full_url)
        else:
            self.instance = UrlShortener.objects.create(
                full_url=full_url, short_code=generate_new_short_code()
            )

        return self.instance

    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)
        internal_data['full_url'] = internal_data['full_url'].strip('/')

        return internal_data

    def to_representation(self, instance):
       representation  = super().to_representation(instance)
       representation['short_url'] = settings.APP_URL + representation['short_code']
       return representation