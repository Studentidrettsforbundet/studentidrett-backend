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
        self.factory = APIRequestFactory()

    def get_response(self, query):
        return global_search(self.factory.get("/search/", {"q": query}))

    def test_specific_club_search(self):
        Club.objects.create(name="Searchable1")
        Club.objects.create(name="Searchable2")
        clubs = Club.objects.all()
        response = self.get_response("clubs/Searchable")
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content.get("results")), len(clubs))
        self.assertEqual(content.get("results"), ClubSerializer(clubs, many=True).data)

    def test_specific_sport_search(self):
        sport = Sport.objects.create(name="Searchable")
        response = self.get_response("sports/Searchable")
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content.get("results")), 1)
        self.assertEqual(content.get("results"), [SportSerializer(sport).data])

    def test_specific_group_search(self):
        group = Group.objects.create(name="Searchable")
        response = self.get_response("groups/Searchable")
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content.get("results")), 1)
        self.assertEqual(content.get("results"), [GroupSerializer(group).data])

    def test_specific_city_search(self):
        City.objects.create(id=42, name="Searchable3", region="")
        response = self.get_response("cities/Searchable")
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content.get("results")), 1)
        self.assertEqual(
            content.get("results"), [{"id": 42, "name": "Searchable3", "region": ""}]
        )

    """
    Because of caching in elasticsearch this test currently does not work
    def test_unspecific_search(self):
        response = self.get_response("Searchable")
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 3)
        self.assertEqual(content[:2], [ClubSerializer(self.clubs).data])
        self.assertEqual(content[3], CitySerializer(self.city).data)
    """

    def test_no_results_unspecific(self):
        response = self.get_response("NothingShouldBeReturnedWhenSearchingForThis")
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content.get("results")), 0)

    def test_no_results_specific(self):
        response = self.get_response(
            "clubs/NothingShouldBeReturnedWhenSearchingForThis"
        )
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content.get("results")), 0)

    def test_invalid_index_specific_search(self):
        response = self.get_response("NothingToLookFor/TestNavn")
        content = loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content.get("results")), 0)
