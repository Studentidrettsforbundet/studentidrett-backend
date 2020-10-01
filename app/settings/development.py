import os

from app.app.enums import EnvironmentOptions

""" GENERAL """
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = False
PRODUCTION = True
ENVIRONMENT = EnvironmentOptions.DEVELOPMENT


""" ACCESS_CONTROL """
ALLOWED_HOSTS = ["kundestyrt-nsi-dev-backend.azurewebsites.net"]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = "https://kundestyrt-nsi-dev-backend.azurewebsites.net"

""" STATIC_FILES """
STATIC_ROOT = os.getenv("STATIC_PATH")
MEDIA_ROOT = os.getenv("MEDIA_PATH")


""" LOGGING NOT YET IMPLEMENTED """
