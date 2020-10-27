from rest_framework import serializers

from app.utils import general_validator, validate_name
from clubs.models import Club


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = [
            "id",
            "city",
            "name",
            "description",
            "contact_email",
            "membership_fee",
            "register_info",
        ]

    def validate(self, data):
        check_fields = ["description", "membership_fee", "register_info"]
        validate_name(data["name"])
        for item in data:
            if item in check_fields:
                general_validator(item, data[item])
        return data
