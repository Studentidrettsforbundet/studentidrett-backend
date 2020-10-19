from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from questionnaire.models import Question
from questionnaire.serializers import AnswerSerializer, QuestionSerializer


class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["get", "post"]

    def create(self, request, *args, **kwargs):
        return self.deduce_recommendation(request)

    def deduce_recommendation(self, request):
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    http_method_names = ["get", "post"]
