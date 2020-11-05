import os

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.serializers import ValidationError

from app.settings.base import GENERAL_VALID_INPUT, NAME_VALID_INPUT


def validate_name(name, field="Name"):
    if not NAME_VALID_INPUT.match(name):
        raise ValidationError(f"{field} must match pattern: {NAME_VALID_INPUT.pattern}")


def general_validator(key, value):
    if value:
        if not GENERAL_VALID_INPUT.match(value):
            raise ValidationError(
                f"{key} must match pattern: {GENERAL_VALID_INPUT.pattern}"
            )


def query_param_invalid(query, raise_exception=True):
    if NAME_VALID_INPUT.match(query):
        return None
    else:
        message = (
            f"Query param '{query}' contains invalid characters."
            f" Query must match regex pattern: {NAME_VALID_INPUT.pattern}"
        )
        if raise_exception:
            raise NotFound(
                detail=message,
                code=status.HTTP_404_NOT_FOUND,
            )
        else:
            return message


def is_allowed_origin(origin):
    env_name = os.getenv("ENV_NAME", "local")
    if env_name == "staging":
        from app.settings.development import CORS_ALLOWED_ORIGINS, CORS_ORIGIN_ALLOW_ALL
    elif env_name == "production":
        from app.settings.production import CORS_ALLOWED_ORIGINS, CORS_ORIGIN_ALLOW_ALL
    else:
        from app.settings.local import CORS_ORIGIN_ALLOW_ALL

    if CORS_ORIGIN_ALLOW_ALL or (origin in CORS_ALLOWED_ORIGINS):
        return True
    else:
        return False
