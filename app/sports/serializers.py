from rest_framework import serializers
from sports.models import Sport


class SportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sport
        fields = ['url', 'name']
