from rest_framework import serializers
from clubSports.models import ClubSport


class ClubSportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClubSport
        fields = ['url', 'name', 'description', 'coverPhoto', 'sportType', 'contactPerson', 'contactMail']
