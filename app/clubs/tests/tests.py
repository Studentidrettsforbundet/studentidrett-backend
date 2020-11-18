import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from cities.factories.city_factories import CityFactory, CityFactoryB
from cities.models import City

# from clubs.factories.club_factories import BIClubFactory, ClubFactory
from clubs.factories.club_factories import BIClubFactory, ClubFactory
from clubs.models import Club
from clubs.serializers import ClubSerializer
from clubs.views import ClubViewSet
from groups.models import Group
from sports.models import Sport

from django.contrib.auth.models import User


def get_response(request, user=None, club_id=None):
    """
    Converts a request to a response.
    :param request: the desired HTTP-request.
    :param user: the user performing the request. None represents an anonymous user
    :param club_id: the desired group. None represents all clubs.
    :return: the HTTP-response from Django.
    """

    force_authenticate(request, user=user)

    if club_id:
        view = ClubViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        )
        return view(request, pk=club_id)
    else:
        view = ClubViewSet.as_view(
            {"get": "list", "put": "update", "delete": "destroy", "post": "create"}
        )
        return view(request)


@pytest.mark.django_db
class TestClubsApi(APITestCase):
    def setUp(self):

        self.name = "NTNUI"

        self.city1 = CityFactory()
        self.club1 = ClubFactory(city=self.city1)
        self.city2 = CityFactoryB()
        self.club2 = BIClubFactory(city=self.city2)

        self.user = User.objects.create_superuser(
            username="testuser", email="testuser@test.com", password="testing"
        )
        self.clubs = Club.objects.all()
        self.factory = APIRequestFactory()

    @pytest.mark.django_db
    def test_club_detail(self):
        request = self.factory.get("/clubs/")
        response = get_response(request, club_id=self.club1.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ClubSerializer(self.club1).data)

    def test_clubs_list(self):
        request = self.factory.get("/clubs/")
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {"count", "next", "previous", "results"})
        self.assertEqual(len(response.data.get("results")), len(self.clubs))
        self.assertEqual(
            response.data.get("results"), ClubSerializer(self.clubs, many=True).data
        )

    def test_club_detail_non_existing(self):
        request = self.factory.get("clubs")
        response = get_response(request, club_id="99")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_param_city(self):
        request = self.factory.get("clubs", {"city": self.city1.name})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
        self.assertEqual(response.data.get("results")[0].get("city"), self.city1.pk)

    def test_query_param_city_id(self):
        request = self.factory.get("clubs", {"city": self.city1.pk})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
        self.assertEqual(response.data.get("results")[0].get("city"), self.city1.pk)

    def test_query_param_city_no_clubs(self):
        City(name="Oslo")
        request = self.factory.get("clubs", {"city": "Oslo"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 0)

    def test_query_param_non_existing_city(self):
        request = self.factory.get("/clubs/", {"city": "Gotham"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 0)

    def test_invalid_query_param(self):
        request = self.factory.get("/groups/", {"sport": "Sp@rt"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_param_sport(self):
        sport = Sport.objects.create(name="TestSport")
        group = Group.objects.create(name="TestGroup", club=self.club1)
        group.sports.add(sport)
        request = self.factory.get("/clubs/", {"sport": "TestSport"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
        self.assertEqual(
            response.data.get("results")[0], ClubSerializer(self.club1).data
        )

    def test_query_param_sport_id(self):
        sport = Sport.objects.create(name="TestSport")
        group = Group.objects.create(name="TestGroup", club=self.club1)
        group.sports.add(sport)
        request = self.factory.get("/clubs/", {"sport": sport})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
        self.assertEqual(
            response.data.get("results")[0], ClubSerializer(self.club1).data
        )

    def test_query_param_sport_no_clubs(self):
        request = self.factory.get("/clubs/", {"sport": "Dans"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 0)

    def test_post_club(self):
        request = self.factory.post(
            "/clubs/",
            {
                "name": "GCIL",
                "city": self.city1.pk,
                "description": "Lover max guttastemning",
                "contact_email": "styret@gc.no",
            },
            format="json",
        )
        response = get_response(request, user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Club.objects.filter(name="GCIL").exists())

    def test_post_club_auth(self):
        request = self.factory.post(
            "/clubs/",
            {
                "name": "GCIL2",
                "city": self.city1.pk,
                "description": "Lover max guttastemning",
                "contact_email": "styret@gc.no",
            },
            format="json",
        )
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Club.objects.filter(name="GCIL2").exists())

    def test_invalid_name(self):
        request = self.factory.post("/clubs/", {"name": "Club%3"}, format="json")
        response = get_response(request, user=self.user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_char_field(self):
        request = self.factory.post(
            "/clubs/",
            {"name": "Clubbb", "description": "This description i$ not valid"},
            format="json",
        )
        response = get_response(request, user=self.user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
