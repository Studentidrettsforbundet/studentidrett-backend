from rest_framework import serializers

from questionnaire.models import Label
from questionnaire.serializers import LabelSerializer
from sports.models import Sport


class SportSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)

    class Meta:
        model = Sport
        fields = ["id", "name", "labels"]

    def create(self, validated_data):
        new_labels = validated_data.pop("labels")
        existing_sports = [
            x.get("name") for x in SportSerializer(Sport.objects.all(), many=True).data
        ]
        sport_exists = validated_data.get("name") in existing_sports
        if not sport_exists:
            sport = Sport.objects.create(**validated_data)
        else:
            sport = Sport.objects.get(name=validated_data.get("name"))
        for label in new_labels:
            existing_label = Label.objects.filter(text=label.get("text")).first()
            if existing_label is not None:
                existing_label.sports.add(sport)
            else:
                lab = Label.objects.create(text=label.get("text"))
                lab.sports.add(sport)
        return sport
