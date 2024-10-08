# my_project/settings/prod.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com']
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "http://yourdomain.com",
]
# Production-specific settings
