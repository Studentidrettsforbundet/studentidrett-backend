from .models import Club
from rest_framework import serializers
from django.contrib.auth.models import User


class ClubSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Club
        fields = ['url', 'id', 'owner', 'name', 'contact_email', 'contact_phone', 'pricing', 'register_info']
        """
            The source argument controls which attribute is used to populate a field, 
            and can point at any attribute on the serialized instance.
        """

class UserSerializer(serializers.HyperlinkedModelSerializer):
    clubs = serializers.HyperlinkedRelatedField(many = True, view_name='club-detail', queryset=Club.objects.all())

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'clubs']

