from rest_framework import serializers
from groups.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'cover_photo', 'sport_type', 'club', 'city'] #, 'contact_person', 'contact_email']
