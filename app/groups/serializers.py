from rest_framework import serializers
from clubSports.models import ClubSport


class ClubSportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubSport
        fields = ['id', 'name', 'description', 'cover_photo', 'sport_type', 'club', 'contact_person', 'contact_email']
