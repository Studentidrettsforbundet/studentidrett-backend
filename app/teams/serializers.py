from rest_framework import serializers
from teams.models import Team, Schedule, TryoutDates


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'date']


class TryoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TryoutDates
        fields = ['id', 'date']


class TeamSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer(many=True)
    tryout_dates = TryoutSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'location', 'group', 'sport', 'description', 'cost', 'equipment', 'gender',
                  'skill_level', 'season', 'schedule', 'tryout_dates', 'facebook_link', 'availability', 'image']

    def create(self, validated_data):
        schedules = validated_data.pop('schedule')
        tryout_dates = validated_data.pop('tryout_dates')
        team = Team.objects.create(**validated_data)
        for date in schedules:
            Schedule.objects.create(date=date.get("date"))
        for date in tryout_dates:
            TryoutDates.objects.create(date=date.get("date"))
        return team
