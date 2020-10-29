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
