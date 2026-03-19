"""Test settings."""
from .base import *  # noqa: F401, F403

DEBUG = False

# Faster password hashing for tests
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

# In-memory cache for tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
