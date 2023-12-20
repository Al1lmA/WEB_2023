"""
Django settings for bmstu_lab project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-81o@&-e99=uba%s1a9fl^6=(+x-=6wskrpt@4po4iu*bz_7c_5'

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

    'bank_services',
    
    # DRF
    'rest_framework',

    'django.contrib.staticfiles',  #Необходим для  swagger ui's css/js файлов (По умолчанию включен)
    'drf_yasg',
]

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticatedOrReadOnly',
#     ],
# }

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

AUTH_USER_MODEL = 'bank_services.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'bmstu_lab.urls'

CORS_ALLOWED_ORIGINS = [
    # Frontend
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Backend
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']

CORS_ALLOWED_URLS = [
    r"^/services/$",
    r"^/services/\d+/$",

]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_CREDENTIALS = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "bmstu_lab/templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bmstu_lab.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bank_servicesN',
        'USER': 'admin',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': 5432, # Стандартный порт PostgreSQL
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/bmstu_lab/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ADMINS = (
  ('admin', 'zhdanova.yana2003@yandex.ru'),
)

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'bankservices'
AWS_ACCESS_KEY_ID = 'AaoDCT0HL7KEUYVEA5wh'
AWS_SECRET_ACCESS_KEY = 'eSWrPjBNLFfJ1kFmdnxekKqcHAgdZnJWvsW0mb9H'
AWS_S3_ENDPOINT_URL = 'http://127.0.0.1:9000'
AWS_S3_ENDPOINT_URL = 'http://192.168.200.156:9000'
PASSWORD_ACYNC = "12345"