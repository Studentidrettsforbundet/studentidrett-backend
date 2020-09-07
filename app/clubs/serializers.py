from rest_framework import serializers

from clubs.models import Club


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'city', 'name', 'information', 'contact_email', 'contact_phone', 'pricing', 'register_info']
