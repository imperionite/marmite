import os
from decouple import config, Csv
import dj_database_url # type: ignore
from pathlib import Path
from datetime import timedelta
from django.conf import settings
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='secretkey')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost, 127.0.0.1, host.docker.internal, marmite.onrender.com', cast=Csv())


# Application definition & Middlewares
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'corsheaders',
    'django_filters',
    'social_django',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'djoser',
    'drf_spectacular',
    'whitenoise.runserver_nostatic',
]

LOCAL_APPS = [
    'posts.apps.PostsConfig',
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


# Common & Templates
# ------------------------------------------------------------------------------
AUTH_USER_MODEL = "posts.User"

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
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

# Static files (For Django Admin)
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


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
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# CORS
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOW_CREDENTIALS = True

CORS_EXPOSE_HEADERS = ['Content-Type', 'authorization', 'X-CSRFToken', 'Access-Control-Allow-Origin: *',]

CORS_ALLOWED_ORIGINS = [
    'https://localhost:8080',
    'https://127.0.0.1:8080',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'https://marmite.onrender.com',
]

CORS_ORIGIN_WHITELIST = (
    'https://localhost:8080',
    'https://127.0.0.1:8080',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'https://marmite.onrender.com',
)

CORS_ALLOW_HEADERS = default_headers + (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)


CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]


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
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        'rest_framework.permissions.AllowAny'
    ],
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']

}

# Django-Allauth
# ------------------------------------------------------------------------------

REST_USE_JWT = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_METHODS = ['email']
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['email', 'profile', 'openid'],
        'AUTH_PARAMS': {'access_type': 'offline'},
        'OAUTH_PKCE_ENABLED': True,
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
        }
    }
}

LOGIN_REDIRECT_URL = config(
    'LOGIN_REDIRECT_URL', default='http://127.0.0.1:5173/dashboard')

SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

# Google Credentials
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('GOOGLE_CLIENT_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]

SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']

# Simple JWT
# ------------------------------------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=180),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'SIGNING_KEY': config('SIGNING_KEY', default='insecure-default-key'),  # Replace with a secure key from env!
    'ALGORITHM': 'HS256',
    'TOKEN_OBTAIN_SERIALIZER': 'posts.serializers.CustomTokenObtainPairSerializer',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID')

GOOGLE_SECRET = config('GOOGLE_CLIENT_SECRET')

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'jwt-auth',
}

# Djoser
# ------------------------------------------------------------------------------

DJOSER = {
    'LOGIN_FIELD': 'identifier',
    'SERIALIZERS': {
        'user_create': 'posts.serializers.UserSerializer',
        'user': 'posts.serializers.UserSerializer',  # Use custom serializer for user retrieval as well
    },
    'AUTH_BACKENDS': (
        'posts.backends.EmailOrUsernameModelBackend',
    ),
}



# Security
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = False

X_FRAME_OPTIONS = 'DENY'

CSRF_COOKIE_HTTPONLY = False

CSRF_TRUSTED_ORIGINS = [
        'http://127.0.0.1:8000',
        'https://127.0.0.1:8080',
        'https://localhost:8080',
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'https://marmite.onrender.com',
]

if not settings.DEBUG:

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    SECURE_SSL_REDIRECT = config(
        'SECURE_SSL_REDIRECT', default=True, cast=bool)

    SESSION_COOKIE_SECURE = config(
        'SESSION_COOKIE_SECURE', default=True, cast=bool)

    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE',
                                default=True, cast=bool)

    SECURE_HSTS_SECONDS = config(
        'SECURE_HSTS_SECONDS', default=18408206, cast=int)  # 60

    SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
        'SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)

    SECURE_HSTS_PRELOAD = config(
        'SECURE_HSTS_PRELOAD', default=True, cast=bool)

    SECURE_CONTENT_TYPE_NOSNIFF = config(
        'SECURE_CONTENT_TYPE_NOSNIFF', default=True, cast=bool)

    

    