# my_project/settings/dev.py
from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins in development
# Development-specific settings
