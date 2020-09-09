from rest_framework import serializers
from sports.models import Sport


class SportSerializer(serializers.HyperlinkedModelSerializer):
    model = Sport
    fields = ['name']
