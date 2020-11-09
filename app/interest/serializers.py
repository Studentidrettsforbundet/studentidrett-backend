from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Interest


class InterestSerializer(serializers.ModelSerializer):
    session_id = serializers.CharField()

    class Meta:
        model = Interest
        fields = ["id", "session_id", "group", "created"]
        validators = [
            UniqueTogetherValidator(
                queryset=Interest.objects.all(), fields=["session_id", "group"]
            )
        ]
