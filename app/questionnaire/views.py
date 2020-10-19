from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from questionnaire.models import Alternative, Answer, Question
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
        for data in request.data:
            answer = int(data.get("answer"))
            if answer < 0 or answer > 4:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return self.deduce_recommendation(request)

    def deduce_recommendation(self, request):
        result_dict = self.get_weighting(request)
        headers = self.get_success_headers(request)

        return Response(result_dict, status=status.HTTP_200_OK, headers=headers)

    def get_weighting(self, request):
        # Counts how many answers correspond to each label and assigns a weight based on answer
        # Return a dictionary of label: weight
        result_dict = dict()
        weighting_dict = dict()
        for data in request.data:
            alternatives = AlternativeSerializer(
                Alternative.objects.filter(qid=data["qid"]), many=True
            )
            for x in range(0, 2):
                ans = int(data.get("answer"))
                labels = alternatives.data[x].get("labels")
                for label in labels:
                    weighting_dict[label.get("text")] = (
                        1 - (0.25 * ans) if x == 0 else 0.25 * ans
                    )
            labels = [
                y.get("text")
                for i in (x.get("labels") for x in alternatives.data)
                for y in i
            ]
            for label in labels:
                result_dict[label] = result_dict.get(label, 0) + weighting_dict.get(
                    label
                )
        return result_dict


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
