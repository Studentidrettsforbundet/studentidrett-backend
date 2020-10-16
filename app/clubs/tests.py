from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from cities.models import City
from clubs.models import Club
from clubs.serializers import ClubSerializer
from clubs.views import ClubViewSet

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


class TestClubsApi(APITestCase):
    def setUp(self):

        self.name = "NTNUI"
        self.city1 = City.objects.create(name="Trondheim", region="MIDT")
        self.city2 = City.objects.create(name="Eiksmarka", region="ØST")
        self.club1 = Club.objects.create(
            name=self.name,
            city=self.city1,
            description="This is a club for the best of the best!",
            contact_email="captain1@ntnui.com",
            membership_fee="about half of your yearly income",
            register_info="You'll have to sell your soul, and bake a cake",
        )

        Club.objects.create(
            name="BI lions",
            city=self.city2,
            description="We just wanna take your money",
            contact_email="cheif@bilions.com",
            membership_fee="about all of your yearly income",
            register_info="You'll have to buy champagne for the whole club",
        )

        self.user = User.objects.create_superuser(
            username="testuser", email="testuser@test.com", password="testing"
        )
        self.clubs = Club.objects.all()
        self.factory = APIRequestFactory()

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

    def test_query_param_city_no_clubs(self):
        City(name="Oslo")
        request = self.factory.get("clubs", {"city": "Oslo"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 0)

    def test_query_param_non_existing_city(self):
        request = self.factory.get("clubs", {"city": "Gotham"})
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
