"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l7oo_)!&o#0q4rc%)*vx9%31ioit7w&#0c0!2%@%^pf=ntt47j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'api',
    'rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
    'drf_yasg',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/
# databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'madina-tic',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Algiers'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/api/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/api/media/'

# Django Rest Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': 'django_filters.rest_framework.DjangoFilterBackend',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated', ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# CORS Configuration
CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://frontend:3000',
    'http://0.0.0.0:3000',
)

# User auth model
AUTH_USER_MODEL = 'api.User'

# Email backend settings for Django
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_HOST_USER = 'oussamamessabih02@gmail.com'
EMAIL_HOST_PASSWORD = 'MN9mFhITLvYE3Afd'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Registration settings
REST_SESSION_LOGIN = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SITE_ID = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_USERNAME_REQUIRED = False
OLD_PASSWORD_FIELD_ENABLED = True

AUTHENTICATION_BACKENDS = (
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Custom Registration config
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "api.serializers.CustomRegisterSerializer",
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'api.serializers.UserProfileSerializer',
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    "DEFAULT_GENERATOR_CLASS": "rest_framework.schemas.generators.BaseSchemaGenerator",
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
}

PUSHER_APP_ID = u"1014450"
PUSHER_KEY = u"eb1d3c82c04cfd3f2990"
PUSHER_SECRET = u"41a025f661325e1a7672"
PUSHER_CLUSTER = u"eu"

ADMINS = [('abdelwahed', 'a.madaniyousfi@esi-sba.dz'), ('oussama', 'o.messabih@esi-sba.dz'), ('djawed', 'roiacult27@gmail.com'), ('moncef', 'm.reggam@esi-sba.dz'), ('oussamabng', 'oussamabngdev@gmail.com'), ('said', 's.bouaballah@esi-sba.dz')]

DEFAULT_FROM_EMAIL = 'admin@madina-tic.ml'