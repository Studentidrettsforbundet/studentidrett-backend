from rest_framework import serializers
from teams.models import Team, Schedule, TryoutDates


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'date']


class TryoutDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TryoutDates
        fields = ['id', 'date']


class TeamSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer(many=True, allow_null=True)
    tryout_dates = TryoutDatesSerializer(many=True, allow_null=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'location', 'group', 'sport', 'description', 'cost', 'equipment', 'gender',
                  'skill_level', 'season', 'schedule', 'tryout_dates', 'facebook_link', 'availability', 'image']
