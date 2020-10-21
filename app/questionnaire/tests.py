import math

from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from questionnaire.models import Alternative, Label, Question
from questionnaire.recommendation_engine import RecommendationEngine
from questionnaire.views import QuestionnaireViewSet
from sports.models import Sport


class TestQuestionnaireAPI(APITestCase):
    def setUp(self):
        self.post_view = QuestionnaireViewSet.as_view({"post": "create"})
        self.factory = APIRequestFactory()
        q = Question.objects.create(text="spm")
        alt1 = Alternative.objects.create(qid=q, text="alternative1")
        alt2 = Alternative.objects.create(qid=q, text="alternative2")
        self.sport1 = Sport.objects.create(name="sport1")
        self.sport2 = Sport.objects.create(name="sport2")
        lab1 = Label.objects.create(text="label1")
        lab2 = Label.objects.create(text="label2")
        lab1.alternatives.add(alt1)
        lab2.alternatives.add(alt2)
        lab1.sports.add(self.sport1)
        lab2.sports.add(self.sport2)

        self.qid1 = q.pk
        self.answer1 = 2

    def test_post_questionnaire(self):
        request = self.factory.post(
            "/questionnaire/",
            [{"qid": self.qid1, "answer": self.answer1}],
            format="json",
        )
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {"recommendation", "confidence"})
        self.assertEqual(
            response.data.get("recommendation"),
            [
                {
                    "name": "sport1",
                    "id": self.sport1.pk,
                    "score": round(math.sqrt(0.5), 3),
                },
                {
                    "name": "sport2",
                    "id": self.sport2.pk,
                    "score": round(math.sqrt(0.5), 3),
                },
            ],
        )


class TestRecommenderEngine(TestCase):
    def setUp(self):
        self.qid1 = 1
        self.answer1 = 3
        self.post_view = QuestionnaireViewSet.as_view({"post": "create"})
        self.factory = APIRequestFactory()
        request = self.factory.post(
            "/questionnaire/", {"qid": self.qid1, "answer": self.answer1}, format="json"
        )
        self.recom = RecommendationEngine(request)

    def test_distance_fn(self):
        list1 = [0, 1, 0, 1]
        list2 = [0.5, 0.5, 0, 1]
        self.assertEqual(self.recom.distance_fn(list1, list2), round(math.sqrt(0.5), 3))
