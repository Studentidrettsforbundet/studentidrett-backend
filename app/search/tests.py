from json import loads

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from cities.models import City
from cities.serializers import CitySerializer
from clubs.models import Club
from clubs.serializers import ClubSerializer
from groups.models import Group
from groups.serializers import GroupSerializer
from search.views import global_search
from sports.models import Sport
from sports.serializers import SportSerializer


class TestClubsApi(APITestCase):
    def setUp(self):
        self.club1 = Club.objects.create(name="TestNavn1")
        Club.objects.create(name="TestNavn2")
        self.city = City.objects.create(name="TestNavn3")

        self.factory = APIRequestFactory()
        self.clubs = Club.objects.all()

    def get_response(self, query):
        return global_search(self.factory.get("/search/", {"q": query}))

    def test_specific_club_search(self):
        response = self.get_response("clubs/TestNavn")
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), len(self.clubs))
        self.assertEqual(content, ClubSerializer(self.clubs, many=True).data)

    def test_specific_sport_search(self):
        sport = Sport.objects.create(name="TestNavn")
        response = self.get_response("sports/TestNavn")
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 1)
        self.assertEqual(content, SportSerializer(sport).data)

    def test_specific_group_search(self):
        group = Group.objects.create(name="TestNavn")
        response = self.get_response("groups/TestNavn")
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 1)
        self.assertEqual(content, GroupSerializer(group).data)

    def test_specific_city_search(self):
        response = self.get_response("cities/TestNavn")
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 1)
        self.assertEqual(content, CitySerializer(self.city).data)

    def test_unspecific_search(self):
        response = self.get_response("TestNavn")
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 3)
        self.assertEqual(content[:2], ClubSerializer(self.clubs).data)
        self.assertEqual(content[3], CitySerializer(self.city).data)
