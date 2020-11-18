# flake8: noqa


if os.getenv("GITHUB_WORKFLOW"):

    ELASTICSEARCH_DSL = {
        "default": {"hosts": "elasticsearch"},
    }
else:
    from .local import *

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
