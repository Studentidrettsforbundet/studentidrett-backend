from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from sports.models import Sport
from questionnaire.models import Questionnaire
from questionnaire.views import QuestionnaireViewSet


class TestQuestionnaireAPI(APITestCase):

    def setUp(self):

        self.qna1 = (0, 0.25)
        self.qna2 = (1, 0.5)
        self.qna3 = (2, 1)

        self.questionnaire1 = Questionnaire.objects.create(
            qna=[self.qna1]
        )
        self.factory = APIRequestFactory()

    def test_post_questionnaire(self):
        request = self.factory.post(
            "/questionnaire/", {"qna": self.qna1}, format="json"
        )
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.keys(), {"id", "qna", "created"})

