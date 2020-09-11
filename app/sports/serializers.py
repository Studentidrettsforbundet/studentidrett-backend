from rest_framework import serializers
from sports.models import Sport


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ['id', 'name']
