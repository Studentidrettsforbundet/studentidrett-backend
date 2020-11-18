# flake8: noqa
from .local import *

ELASTICSEARCH_DSL = {
    "default": {"hosts": "localhost:9200"},
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "HOST": "localhost",
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "PORT": "5432",
    }
}
