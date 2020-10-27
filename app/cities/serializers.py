from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.utils import validate_name
from cities.models import City
from clubs.models import Club


class CitySerializer(serializers.ModelSerializer):
    clubs = serializers.StringRelatedField(many=True, read_only=True)
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Club.objects.all())]
    )

    class Meta:
        model = City
        fields = ["id", "name", "region", "clubs"]

    def validate(self, data):
        validate_name(data["name"])
        return data
