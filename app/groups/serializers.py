from rest_framework import serializers

from app.utils import general_validator, validate_name
from groups.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "description",
            "cover_photo",
            "sports",
            "club",
            "city",
            "contact_email",
        ]

    def validate(self, data):
        validate_name(data["name"])
        general_validator("description", data["description"])
        return data
