from .models import Club
from rest_framework import serializers


class ClubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = ['url', 'id', 'name', 'contact_email', 'contact_phone', 'pricing', 'register_info']
        """
            The source argument controls which attribute is used to populate a field, 
            and can point at any attribute on the serialized instance.
        """

