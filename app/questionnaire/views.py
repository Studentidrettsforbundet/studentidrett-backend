from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from app.settings.pagination import CustomPagination
from questionnaire.models import Answer, Question
from questionnaire.recommendation_engine import RecommendationEngine
from questionnaire.serializers import AnswerSerializer, QuestionSerializer


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
        results = recom.calculate()
        headers = self.get_success_headers(request)

        # TODO: Calculate a confidence-score
        return Response(
            {"recommendation": results, "confidence": 0.95},
            status=status.HTTP_200_OK,
            headers=headers,
        )


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    http_method_names = ["get", "post"]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        if len(request.data.get("alternatives")) != 2:
            return Response(
                {"message": "There must be exactly 2 alternatives specified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    # Fetch questions currently in database, filtering logic handled in front end
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginated_resp = self.paginate_queryset(queryset)
        serializer = self.serializer_class
        serialized = serializer().list(paginated_resp)
        page = self.get_paginated_response(serialized)
        return page
