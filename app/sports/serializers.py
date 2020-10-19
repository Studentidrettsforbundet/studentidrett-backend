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
        sport = Sport.objects.create(**validated_data)
        for label in new_labels:
            existing_label = Label.objects.filter(text=label.text)
            if len(existing_label) == 1:
                existing_label[0].sports.add(sport)
            else:
                lab = Label.objects.create(text=label.text)
                lab.sports.add(sport)
        return sport
