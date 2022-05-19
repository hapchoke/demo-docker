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


DATABASES = {
    'default': env.db(),
}
# if 'RDS_DB_NAME' in os.environ:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.environ['RDS_DB_NAME'],
#             'USER': os.environ['RDS_USERNAME'],
#             'PASSWORD': os.environ['RDS_PASSWORD'],
#             'HOST': os.environ['RDS_HOSTNAME'],
#             'PORT': os.environ['RDS_PORT'],
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': 'postgres',
#             'USER': 'postgres',
#             'PASSWORD': 'postgres',
#             'HOST': 'db',
#             'PORT': '5432',
#         }
#     }
