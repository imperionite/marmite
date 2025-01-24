import os
from decouple import config, Csv
import dj_database_url # type: ignore
from pathlib import Path
from datetime import timedelta
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='secretkey')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost, 127.0.0.1, connectly-api, host.docker.internal', cast=Csv())



# Application definition & Middlewares
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    "django.contrib.sites",
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'djoser',
]

LOCAL_APPS = [
    'posts.apps.PostsConfig',
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Common & Templates
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "posts.User"

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SITE_ID = 1

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'


# Database & Cache
# ------------------------------------------------------------------------------
db_from_env = config('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(
        default=db_from_env,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Disable server-side cursors when using PgBouncer in transaction pooling mode
DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True

# Password & Auth Backends
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

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

# allow to use username or email on user's login 
AUTHENTICATION_BACKENDS = [
    'posts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# CORS
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOW_CREDENTIALS = True

CORS_EXPOSE_HEADERS = ['Content-Type', 'authorization', 'X-CSRFToken', 'Access-Control-Allow-Origin: *',]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'https://127.0.0.1:8080',
    'http://localhost:8000',
    'http://127.0.0.1:8000',

]
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',
    'https://127.0.0.1:8080',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
)

CORS_ALLOW_HEADERS = default_headers + (
    'Access-Control-Allow-Origin',
    'x-csrftoken',
    'x-requested-with',
    'Access-Control-Allow-Origin',
    'cache-control',
    'if-modified-since',
    'keep-alive',
    'X-Mx-ReqToken',
    'XMLHttpRequest',
)

CORS_PREFLIGHT_MAX_AGE = 86400

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = config('ADMIN_URL', default='admin/')


# django-rest-framework
# -------------------------------------------------------------------------------

DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + \
        ('rest_framework.renderers.BrowsableAPIRenderer',)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.AllowAny'
    ],
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    # 'PAGE_SIZE': 10,
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']

}

# Djoser
# ------------------------------------------------------------------------------

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user_create': 'posts.serializers.UserSerializer',
        'user': 'posts.serializers.UserSerializer',  # Use custom serializer for user retrieval as well
    },
    'LOGIN_FIELD': 'login',
    'AUTH_BACKENDS': (
        'posts.backends.EmailOrUsernameModelBackend',
    ),
}


# Simple JWT
# ------------------------------------------------------------------------------

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=180),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Security
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = False

X_FRAME_OPTIONS = 'DENY'

CSRF_COOKIE_HTTPONLY = False

CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'

CSRF_COOKIE_NAME = 'csrftoken'

CSRF_COOKIE_SAMESITE = 'Lax'

SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)

SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int) # 1 year

SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)

SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)

CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)

SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default=True, cast=bool)

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='https://localhost:8080', cast=Csv())

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF', default=True, cast=bool)




