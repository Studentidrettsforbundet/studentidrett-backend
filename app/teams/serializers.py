from rest_framework import serializers, permissions
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'full_capacity', 'tryouts', 'registration_open', 'group')