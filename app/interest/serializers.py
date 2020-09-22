from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Interest


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'cookie_key', 'group', 'created']
        validators = [
            UniqueTogetherValidator(
                queryset=Interest.objects.all(),
                fields=['cookie_key', 'group']
            )
        ]
