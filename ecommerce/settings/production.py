from .base import *
import dj_database_url


DEBUG = env.get_value('DEBUG',bool)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]
# STRIPE_SECRET_KEY = env('STRIPE_LIVE_SECRET_KEY')
# STRIPE_PUBLIC_KEY = env('STRIPE_LIVE_PUBLIC_KEY')
# 本番環境だがテスト鍵使う
STRIPE_SECRET_KEY = env('STRIPE_TEST_SECRET_KEY')
STRIPE_PUBLIC_KEY = env('STRIPE_TEST_PUBLIC_KEY')

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
DEFAULT_FILE_STORAGE = 'ecommerce.storage_backends.MediaStorage'

if 'DATABASE_URL' in os.environ:
    DATABASES = {
    'default': env.db(),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'db',
            'PORT': '5432',
        }
    }

# import django_heroku
# django_heroku.settings(locals())