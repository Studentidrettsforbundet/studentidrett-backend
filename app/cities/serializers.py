from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from cities.models import City


class CitySerializer(serializers.ModelSerializer):
    clubs = serializers.StringRelatedField(many=True, read_only=True)
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=City.objects.all())]
    )

    class Meta:
        model = City
        fields = ["id", "name", "region", "clubs"]
