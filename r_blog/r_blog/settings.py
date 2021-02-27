import os
from pathlib import Path

'r_blog settings'

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('secret_key')

DEBUG = True

AUTH_USER_MODEL = 'main.Client'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'easy_thumbnails',
    'django_cleanup',
    'social_django',
    'django_filters',
    'djoser',
    'rest_framework_social_oauth2',
    'oauth2_provider',
    'rest_framework',
    'rest_framework.authtoken',

    'main',
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',  # Обычные токены, которые будут созранятся в базу данных
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # для авторизации с помощью OAUTH2
        'rest_framework_social_oauth2.authentication.SocialAuthentication',  # тоже самое для чего и выше
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend'  # Для фильтрации запросов drf
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # Что будет отвечать за пагинацию на сайте
    'PAGE_SIZE': 5,  # Какое кол-во записей будет выводится на 1 странице
}

# smtp
EMAIL_PORT = os.getenv('email_port')  # Порт через который будут отправляется письма
EMAIL_USE_TLS = True  # Использовать ли протокол шифрования TLS
EMAIL_HOST = os.getenv('email_host')  # Какой протокол SMTP использовать
EMAIL_HOST_USER = os.getenv('email_host_user')  # Почта с которой будут отправлятся все письма
EMAIL_HOST_PASSWORD = os.getenv('email_host_pass')  # Пароль от это почты

DJOSER = {
    """
    Токен для авторизации передается в headers
    Заголовок в headers выглядит примерно так
    Authorization: Token <token>
    """

    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',  # Для подтверждения сброса пароля
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',  # Для подтверждения сброса юзернейма
    'ACTIVATION_URL': '#/activate/{uid}/{token}',  # Ссылка с активацией
    'SEND_ACTIVATION_EMAIL': True,  # Отправлять ли ссылку активации на почту
    'SERIALIZERS': {},
}

ROOT_URLCONF = 'r_blog.urls'

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
                'social_django.context_processors.backends',  # это и одно ниже для регистрации через соц сети
                'social_django.context_processors.login_redirect',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'r_blog.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('db_name'),
        'USER': os.getenv('db_user'),
        'PASSWORD': os.getenv('db_pass'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

#social_auth
SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('vk_key')  # Секретный ключ который берется из приложения вконтакте
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('vk_secret')  # тоже ключ и тоже берется из приложения
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']  # Чтобы дополнительно запросить у пользователя почту
AUTHENTICATION_BACKENDS = (  # Список классов реализующий аутентефикацию и авторизацию
    'social_core.backends.vk.VKOAuth2',  # Это и ниже для авторизации с помощью вк
    'django.contrib.auth.backends.ModelBackend',)

# Thumbnails
THUMBNAIL_ALIASES = {
    '': {
        'default': {
            'size': (201, 201),
            'crop': 'scale',
        }
    }
}
THUMBNAIL_BASEDIR = 'thumbs'

# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# Celery
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_RESULT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
