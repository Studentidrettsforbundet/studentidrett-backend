from rest_framework import serializers

from app.utils import validate_name
from questionnaire.models import Alternative, Answer, Label, Question


class LabelSerializer(serializers.ModelSerializer):
    sports = serializers.StringRelatedField(many=True, read_only=True)
    alternatives = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Label
        fields = ["text", "sports", "alternatives"]

    def validate(self, data):
        validate_name(data["text"], field="Text")
        return data


class AlternativeSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)

    class Meta:
        model = Alternative
        fields = ["text", "labels"]

    def save(self, qid):
        new_labels = self.validated_data.pop("labels")
        alternative = Alternative.objects.create(**self.validated_data, qid=qid)
        for label in new_labels:
            existing_label = Label.objects.filter(text=label.get("text"))
            if len(existing_label) == 1:
                existing_label[0].alternatives.add(alternative)
            else:
                lab = Label.objects.create(text=label.get("text"))
                lab.alternatives.add(alternative)
        return alternative

    def validate(self, data):
        validate_name(data["text"], field="Text")
        return data


class QuestionSerializer(serializers.ModelSerializer):
    alternatives = AlternativeSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "text", "alternatives"]

    def create(self, validated_data):
        alternatives = validated_data.pop("alternatives")
        question = Question.objects.create(**validated_data)
        for alternative in alternatives:
            alt = AlternativeSerializer(data=alternative)
            alt.is_valid()
            alt.save(question)
        return question


    def list(self, validated_data):
        resp = []
        for question in validated_data:
            alternatives = AlternativeSerializer(
                Alternative.objects.filter(qid=question.id), many=True
            )
            # Explicitly define which answer is on which side to keep things consistent
            resp.append(
                {
                    "id": str(question.id),
                    "text": question.text,
                    "left": alternatives.data[0].get("text"),
                    "right": alternatives.data[1].get("text"),
                }
            )
        return resp

    def validate(self, data):
        validate_name(data["text"], "Text")
        return data


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["qid", "answer"]
