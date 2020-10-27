from rest_framework import serializers

from app.utils import general_validator, validate_name
from teams.models import Schedule, Team, TryoutDates


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ["date"]


class TryoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TryoutDates
        fields = ["date"]


class TeamSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer(many=True)
    tryout_dates = TryoutSerializer(many=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "location",
            "group",
            "sport",
            "long_description",
            "short_description",
            "cost",
            "equipment",
            "gender",
            "skill_level",
            "season",
            "schedule",
            "tryout_dates",
            "facebook_link",
            "instagram_link",
            "webpage",
            "availability",
            "image",
        ]

    def create(self, validated_data):
        schedules = validated_data.pop("schedule")
        tryout_dates = validated_data.pop("tryout_dates")
        team = Team.objects.create(**validated_data)
        for date in schedules:
            s = Schedule.objects.create(date=date.get("date"))
            s.team.add(team)
        for date in tryout_dates:
            t = TryoutDates.objects.create(date=date.get("date"))
            t.team.add(team)
        return team

    def validate(self, data):
        check_fields = [
            "long_description",
            "short_description",
            "register_info",
            "cost",
            "equipment",
            "season",
        ]
        validate_name(data["name"])
        for item in data:
            if item in check_fields:
                general_validator(item, data[item])
        return data
