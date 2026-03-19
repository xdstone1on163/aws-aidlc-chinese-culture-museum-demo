"""Development settings."""
from .base import *  # noqa: F401, F403

DEBUG = True

# Dev logging
LOGGING['root']['level'] = 'DEBUG'  # noqa: F405
