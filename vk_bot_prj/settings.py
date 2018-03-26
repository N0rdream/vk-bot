import os
from configurations import Configuration


class Base(Configuration):
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_extensions',
        'bot'
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

    ROOT_URLCONF = 'vk_bot_prj.urls'

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

    WSGI_APPLICATION = 'vk_bot_prj.wsgi.application'

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

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'


class Hosting(Base):

    ALLOWED_HOSTS = ['nordream.ru', 'www.nordream.ru', 'localhost']
    
    CELERY_IMPORTS = ['bot.tasks']
    CELERY_BROKER_URL = 'amqp://localhost:5672//'
    CELERY_REDIS_HOST = os.environ['CELERY_REDIS_HOST']
    CELERY_REDIS_PORT = os.environ['CELERY_REDIS_PORT']
    CELERY_REDIS_DB = os.environ['CELERY_REDIS_DB']
    CELERY_RESULT_BACKEND = f'redis://{CELERY_REDIS_HOST}:{CELERY_REDIS_PORT}/{CELERY_REDIS_DB}'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_SERIALIZER = 'json'

    SECRET_KEY = os.environ['SECRET_KEY']

    DEBUG = True

    STATIC_ROOT = '/home/nordream/vk/vk_bot_django/static/'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['BOT_DATABASE_NAME'],
            'USER': os.environ['BOT_DATABASE_USER'],
            'PASSWORD': os.environ['BOT_DATABASE_PASSWORD'],
            'HOST': os.environ['BOT_DATABASE_HOST'],
            'PORT': os.environ['BOT_DATABASE_PORT']
        }
    }