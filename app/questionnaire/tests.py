from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from sports.models import Sport
from questionnaire.models import Question
from questionnaire.views import QuestionnaireViewSet


class TestQuestionnaireAPI(APITestCase):

    def setUp(self):

        self.qid1 = "1"
        self.answer1 = 3

        self.factory = APIRequestFactory()

    def test_post_questionnaire(self):
        request = self.factory.post(
            "/questionnaire/", {"qid": self.qid1, "answer": self.answer1}, format="json"
        )
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.keys(), {"qid", "answer", "created"})

