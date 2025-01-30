from .base import *  # noqa
from .base import INSTALLED_APPS, MIDDLEWARE

DEBUG = True

# CORS for development
CORS_ALLOW_ALL_ORIGINS = True

# Email for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Debug settings
INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# Debug toolbar settings
INTERNAL_IPS = [
    "127.0.0.1",
]
