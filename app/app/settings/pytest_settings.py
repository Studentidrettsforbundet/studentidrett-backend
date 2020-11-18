# flake8: noqa
import os

if os.getenv("GITHUB_WORKFLOW"):
    from .development import *

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github-actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

    ELASTICSEARCH_DSL = {
        "default": {"hosts": "elasticsearch"},
    }
else:
    from .local import *

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "PORT": "5432",
        }
    }

    ELASTICSEARCH_DSL = {
        "default": {"hosts": os.environ.get("ELASTICSEARCH", "localhost:9200")},
    }
