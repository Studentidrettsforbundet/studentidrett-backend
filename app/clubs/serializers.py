from .models import Club
from rest_framework import serializers
from django.contrib.auth.models import User


class ClubSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Club
        fields = ['id', 'name', 'contact_email', 'contact_phone', 'pricing', 'register_info']
        owner = serializers.ReadOnlyField(source = 'owner.username')
        """
            The source argument controls which attribute is used to populate a field, 
            and can point at any attribute on the serialized instance.
        """

class UserSerializer(serializers.ModelSerializer):
    clubs = serializers.PrimaryKeyRelatedField(many = True, queryset=Club.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'clubs']

