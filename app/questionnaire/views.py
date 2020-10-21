from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from questionnaire.models import Alternative, Answer, Question
from questionnaire.recommendation_engine import RecommendationEngine
from questionnaire.serializers import (
    AlternativeSerializer,
    AnswerSerializer,
    QuestionSerializer,
)


class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        if type(request.data) != list:
            return Response(
                {"message": "Answers must be list-format"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for data in request.data:
            answer = int(data.get("answer"))
            if answer < 0 or answer > 4:
                return Response(
                    {"message": "Each answer must be between 0 and 4"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return self.deduce_recommendation(request)

    def deduce_recommendation(self, request):
        recom = RecommendationEngine(request)
        result_dict, sports_id = recom.calculate()
        headers = self.get_success_headers(request)

        # TODO: Calculate a confidence-score
        return Response(
            {"recommendation": result_dict, "sport_id": sports_id, "confidence": 0.95},
            status=status.HTTP_200_OK,
            headers=headers,
        )


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    http_method_names = ["get", "post"]

    # Fetch questions currently in database, filtering logic handled in front end
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        headers = self.get_success_headers(queryset)
        resp = []
        for question in queryset:
            alternatives = AlternativeSerializer(
                Alternative.objects.filter(qid=question.id), many=True
            )
            if len(alternatives.data) == 2:
                # Explicitly define which answer is on which side to keep things consistent
                resp.append(
                    {
                        "id": str(question.id),
                        "text": question.text,
                        "left": alternatives.data[0].get("text"),
                        "right": alternatives.data[1].get("text"),
                    }
                )
        return Response(resp, status=status.HTTP_200_OK, headers=headers)
