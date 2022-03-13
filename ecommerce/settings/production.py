from .base import *
import dj_database_url



DEBUG = env('DEBUG')
ALLOWED_HOSTS=env.list('ALLOWED_HOSTS')
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]
STRIPE_SECRET_KEY = env('STRIPE_LIVE_SECRET_KEY')
STRIPE_PUBLIC_KEY = env('STRIPE_LIVE_PUBLIC_KEY')

db_from_env = dj_database_url.config()
DATABASES = {
    'default': dj_database_url.config()
}
