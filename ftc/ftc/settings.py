import os

import environ
from datetime import timedelta
from dadataru.tools import DaData
root = environ.Path(__file__) - 2
env = environ.Env()
environ.Env.read_env(env.str(root(), '.env'))

BASE_DIR = root()


DEBUG = env.bool('DEBUG', True)
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.str("ALLOWED_HOSTS", default="").split(" ")
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'drf_yasg',
    'rest_framework',
    'djoser',
    'corsheaders',
    'django_filters',
    'debug_toolbar',
    'rest_framework_simplejwt',
    'django_json_widget',
    'imagekit',

    'common',
    'users',
    'api',
    'events',
    'teams',
    'players',
    'locations',
    'sports',
    'guests',
    'dadataru',
    'sendpulse',
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

MIDDLEWARE += ('crum.CurrentRequestUserMiddleware',)

ROOT_URLCONF = 'ftc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # <- add this line
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

WSGI_APPLICATION = 'ftc.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.NormalNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {
        'create_user': 'users.serializers.UserPostSerializer'
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=31),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=31),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=31),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=31),


}

SPECTACULAR_SETTINGS = {
    'TITLE': 'FTC-Project',
    'DESCRIPTION': 'Free Team Collaboration Project',
    'VERSION': '1.0.0',
}


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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ('users.backends.AuthBackend',)


#############################
#        SENTRY             #
#############################
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)


#############################
#        SWAGGER            #
#############################
SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS":"api.yasg.CustomAutoSchema",
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    'TAGS_SORTER': 'alpha',
}

INTERNAL_IPS = [
    "127.0.0.1",
]


#############################
#       DADATARU            #
#############################
DADATA_API = env('DADATA_API', None)
DADATA_SECRET = env('DADATA_SECRET', None)
dadata = DaData(token=DADATA_API, secret=DADATA_SECRET)

############################
#       SENDPULSE          #
############################
SENDPULSE_ID = env.str('SENDPULSE_ID', default='')
SENDPULSE_SECRET = env.str('SENDPULSE_SECRET', default='')
SENDPULSE_STORAGE = env.str('SENDPULSE_STORAGE', default='FILE')
SENDPULSE_TEMP = env.str('SENDPULSE_TEMP', default='')
SENDPULSE_ROOT = os.path.join(BASE_DIR, 'tmp/')

EMAIL_ADMIN = env.str('EMAIL_ADMIN', default='')
ROBOT_EMAIL = env.str('ROBOT_EMAIL', default='')
ROBOT_NAME = env.str('ROBOT_NAME', default='')


############################
#    PROJECT CUSTOM        #
############################
FRONT_HOST = env.str('FRONT_HOST', default='')
DEFAULT_FIAS_ID = env.str('DEFAULT_FIAS_ID',
                          default='2a1c7bdb-05ea-492f-9e1c-b3999f79dcbc')
