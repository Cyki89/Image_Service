from celery.schedules import crontab
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@bo0@+3u)xagy1e@+yr3$2&%i*t4#2^mek27@4q!7&*%t@78$r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "corsheaders",
    'session_auth',
    'images'
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'images.middlewares.AccountMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "image_db",
        "HOST": "db",
        "PORT": "3306",
        "USER": "root",
        "PASSWORD": "root",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# TEST FOLDERS
TEST_MEDIA_ROOT = BASE_DIR / 'media_test'
TEST_MEDIA_FOLDER = TEST_MEDIA_ROOT / '1'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Other 
PROTOCOL = 'http'
DOMAIN = 'localhost:8000'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
CORS_EXPOSE_HEADERS = ['Accept', 'Content-Type', 'X-CSRFToken']
CORS_ALLOW_CREDENTIALS = True

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"


CELERY_BEAT_SCHEDULE = {
    # 'cleanup_sessions': {
    #     'task': 'images.tasks.cleanup',
    #     'schedule': crontab(minute="*/2"),
    # },
    # 'delete_expire_links': {
    #     'task': 'images.tasks.delete_expire_links',
    #     'schedule': crontab(minute="*/1"),
    # },
}
