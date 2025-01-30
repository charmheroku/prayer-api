from .base import *  # noqa
from .base import BASE_DIR

# Override database settings for local development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Set debug to True for local development
DEBUG = True

# Allow all hosts in local development
ALLOWED_HOSTS = ["*"]

# Disable CORS restrictions in local development
CORS_ALLOW_ALL_ORIGINS = True
