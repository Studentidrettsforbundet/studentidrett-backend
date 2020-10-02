from rest_framework import serializers

from questionnaire.models import Questionnaire


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = [
            "qna"
        ]
