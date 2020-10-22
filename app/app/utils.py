from rest_framework.serializers import ValidationError

from app.settings.base import GENERAL_VALID_INPUT, NAME_VALID_INPUT


def validate_name(name, field="Name"):
    if not NAME_VALID_INPUT.match(name):
        raise ValidationError(f"{field} must match pattern: {NAME_VALID_INPUT.pattern}")


def general_validator(key, value):
    if not GENERAL_VALID_INPUT.match(value):
        raise ValidationError(
            f"{key} must match pattern: {GENERAL_VALID_INPUT.pattern}"
        )


def query_param_valid(query):
    if not NAME_VALID_INPUT.match(query):
        return False
    else:
        return True
