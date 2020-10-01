import os

from app.app.enums import EnvironmentOptions

""" GENERAL """
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = False
PRODUCTION = True
ENVIRONMENT = EnvironmentOptions.PRODUCTION


""" ACCESS_CONTROL """
ALLOWED_HOSTS = []
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = ()

""" STATIC_FILES """
STATIC_ROOT = os.getenv("STATIC_PATH")
MEDIA_ROOT = os.getenv("MEDIA_PATH")


""" LOGGING NOT YET IMPLEMENTED """
