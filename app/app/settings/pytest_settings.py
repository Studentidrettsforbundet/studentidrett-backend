# flake8: noqa
from .local import *

if os.getenv("GITHUB_WORKFLOW"):

    ELASTICSEARCH_DSL = {
        "default": {"hosts": "elasticsearch"},
    }
else:
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

    ELASTICSEARCH_DSL = {
        "default": {"hosts": "localhost:9200"},
    }
