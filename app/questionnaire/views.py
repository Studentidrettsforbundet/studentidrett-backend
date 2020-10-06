from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from questionnaire.models import Question, Answer
from questionnaire.serializers import QuestionSerializer, AnswerSerializer


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
