from rest_framework import serializers

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
            "pricing",
            "register_info",
        ]
