# social_media_api/settings_prod.py
from social_media_api.settings import *   # import base settings

import os
from pathlib import Path
import dj_database_url

DEBUG = False

# Hosts
ALLOWED_HOSTS = ['your-app.herokuapp.com', 'your-domain.com']  # add real domains

# Security
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']  # must be set in env
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True   # if behind HTTPS

# Database
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Static & media
STATIC_ROOT = BASE_DIR / 'staticfiles'   # for collectstatic
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# WhiteNoise (if used)
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware',
              'whitenoise.middleware.WhiteNoiseMiddleware',
              *MIDDLEWARE]  # prepend whitenoise

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# REST framework note: leave auth classes as you had them
