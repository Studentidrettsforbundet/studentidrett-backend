# flake8: noqa
from .base import *

""" GENERAL """
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = False
PRODUCTION = True
ENVIRONMENT = EnvironmentOptions.DEVELOPMENT


""" ACCESS_CONTROL """
ALLOWED_HOSTS = [
    "https://kundestyrt-nsi-backend-staging.azurewebsites.net/",
]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = (
    "https://kundestyrt-nsi-backend-staging.azurewebsites.net/",
    "https://kundestyrt-nsi-frontend-staging.azurewebsites.net/",
)

SECURE_SSL_REDIRECT = True


""" STATIC_FILES """
# STATIC_ROOT = os.getenv("STATIC_PATH")
# MEDIA_ROOT = os.getenv("MEDIA_PATH")
