import os

from app.app.enums import EnvironmentOptions

""" GENERAL """
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY", "This is a random secret key, used for local development only"
)
ENVIRONMENT = EnvironmentOptions.LOCAL


""" ACCESS CONTROL """
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
