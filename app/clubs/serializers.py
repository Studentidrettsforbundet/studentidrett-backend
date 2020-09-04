from .models import Club
from rest_framework import serializers

class ClubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = ['id', 'name', 'contact_email', 'contact_phone', 'pricing', 'register_info']
