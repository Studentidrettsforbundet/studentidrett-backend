from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from cities.models import City
from clubs.models import Club
from sports.models import Sport
from sports.serializers import SportSerializer
from sports.views import SportViewSet
from sports.models import Sport

from django.contrib.auth.models import User


def get_response(request, user=None, sport_id=None):
    """
    Converts a request to a response.
    :param request: the desired HTTP-request.
    :param user: the user performing the request. None represents an anonymous user
    :param group_id: the desired group. None represents all groups.
    :return: the HTTP-response from Django.
    """

    force_authenticate(request, user=user)

    if sport_id:
        view = SportViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        )
        return view(request, pk=sport_id)
    else:
        view = SportViewSet.as_view(
            {"get": "list", "put": "update", "delete": "destroy", "post": "create"}
        )
        return view(request)

class SportModelTest(TestCase):
    def setUp(self):
        sport1 = Sport.object.create(
            name="Sport1"
        )
        sport2 = Sport.object.create(
            name="Sport2"
        )
        sport3 = Sport.object.create(
            name="Sport3"
        )

        sport1.save()
        sport2.save()
        sport3.save()

    def test_sport_attributes(self):
        sport = Sport.object.get(name="Sport1")

        self.assertEqual(sport.name, "Sport1")

    def test_sport_list(self):
        sports = Sport.object.all()

        self.assertEqual(len(sports), not 1)


class SportViewTest(TestCase):
    def setUp(self):
        self.user = User.object.create_superuser(
            username="testuser", email="testuser@test.com", password="testing"
        )
        self.sport = Sport.objects.create(
            name="Sport1"
        )
        self.sports = Sport.objects.all()
        self.factory = APIRequestFactory()

    def test_sport_contains_expected_fields(self):
        request  = self.factory.get("/sports/")
        force_authenticate(request, self.user)
        response = get_response(request, sport_id=self.sport.pk)

        self.assertEqual(
            response.data.keys(),
            {
                "name"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sport_detail(self):
        request = self.factory.get("/sports/")
        response = get_response(request, sport_id=self.sport.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {"count", "next", "previous", "results"})
        self.assertEqual(len(response.data.get("results")), len(self.sports))
        self.assertEqual(
            response.data.get("results"), SportSerializer(self.sports, many=True).data
        )

    def test_nonexistent_group(self):
        request = self.factory.get("/sports/")
        response = get_response(request, sport_id="69")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_group(self):
        request = self.factory.post(
            "/sports/",
            {
                "name": "Sport2"
            },
            format="json"
        )
        response = get_response(request, user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Sport.objects.filter(name="Sport2").exists())

    def test_post_sport_auth(self):
        request = self.factory.post(
            "/sports/",
            {
                "name": "Sport3"
            },
            format="json"
        )
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Sport.object.filter(name="Sport3").exists())

    def test_query_param_city(self):
        request = self.factory.get("/sports/", {"city": self.city.name})



















