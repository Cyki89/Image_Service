import random, string
from .models import UrlShortener
from django.conf import settings


ALLOWED_CHARS = string.ascii_letters + string.digits


def generate_random_short_code(length=settings.SHORT_CODE_LENGTH):
    return ''.join(random.choices(ALLOWED_CHARS, k=length)) 


def generate_new_short_code():
    short_code = generate_random_short_code()
    while UrlShortener.objects.filter(short_code=short_code).exists():
        short_code = generate_random_short_code()

    return short_code