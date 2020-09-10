from rest_framework import serializers

from cities.models import City


class CitySerializer(serializers.ModelSerializer):
    clubs = serializers.StringRelatedField(many=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'region', 'clubs']
