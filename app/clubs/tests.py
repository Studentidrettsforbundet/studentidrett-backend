from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from cities.models import City
from clubs.models import Club
from clubs.views import ClubViewSet

from django.contrib.auth.models import User


class TestClubsApi(APITestCase):
    def setUp(self):

        self.name = "NTNUI"
        self.city1 = City.objects.create(name="Trondheim", region="MIDT")
        self.city2 = City.objects.create(name="Eiksmarka", region="ØST")
        self.description = "This is a club for the best of the best!"
        self.contact_email = "captain1@ntnui.com"
        self.pricing = "about half of your yearly income"
        self.register_info = "You'll have to sell your soul, and bake a cake"

        self.club1 = Club.objects.create(
            name=self.name,
            city=self.city1,
            description="This is a club for the best of the best!",
            contact_email="captain1@ntnui.com",
            pricing="about half of your yearly income",
            register_info="You'll have to sell your soul, and bake a cake",
        )

        Club.objects.create(
            name="BI lions",
            city=self.city2,
            description="We just wanna take your money",
            contact_email="cheif@bilions.com",
            pricing="about all of your yearly income",
            register_info="You'll have to buy champagne for the whole club",
        )

        self.user = User.objects.create_superuser(
            username="testuser", email="testuser@test.com", password="testing"
        )
        self.user.save()

        self.factory = APIRequestFactory()
        self.post_view = ClubViewSet.as_view({"post": "create"})

    def test_club_model(self):
        clubs = Club.objects.all()[1]
        self.assertEqual(clubs.name, self.name)
        self.assertEqual(clubs.city, self.city1)
        self.assertEqual(clubs.description, self.description)
        self.assertEqual(clubs.contact_email, self.contact_email)
        self.assertEqual(clubs.pricing, self.pricing)
        self.assertEqual(clubs.register_info, self.register_info)

    def test_clubs_list(self):
        request = self.factory.get("/clubs/")
        view = ClubViewSet.as_view({"get": "list"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {"count", "next", "previous", "results"})
        self.assertEqual(
            response.data.get("results")[1].keys(),
            {
                "id",
                "city",
                "name",
                "description",
                "contact_email",
                "pricing",
                "register_info",
            },
        )
        self.assertEqual(len(response.data.get("results")), 2)

    def test_club_detail(self):
        request = self.factory.get("/clubs/")
        view = ClubViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.club1.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.keys(),
            {
                "id",
                "city",
                "name",
                "description",
                "contact_email",
                "pricing",
                "register_info",
            },
        )

    def test_club_detail_non_existing(self):
        request = self.factory.get("clubs")
        view = ClubViewSet.as_view({"get": "retrieve"})
        response = view(request, pk="999")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_param_city(self):
        request = self.factory.get("clubs", {"city": self.city1.name})
        view = ClubViewSet.as_view({"get": "list"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
        self.assertEqual(response.data.get("results")[0].get("city"), self.city1.pk)

    def test_query_param_city_no_clubs(self):
        new_city = City(name="Oslo")
        new_city.save()
        request = self.factory.get("clubs", {"city": "Oslo"})
        view = ClubViewSet.as_view({"get": "list"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 0)

    def test_post_club(self):
        city = City.objects.create(name="Bergen")
        request = self.factory.post(
            "/clubs/",
            {
                "name": "GCIL",
                "city": city.id,
                "description": "Lover max guttastemning",
                "contact_email": "styret@gc.no",
            },
            format="json",
        )
        force_authenticate(request, self.user)
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Club.objects.filter(name="GCIL").exists())

    def test_post_club_auth(self):
        city = City.objects.create(name="Bergen")
        request = self.factory.post(
            "/clubs/",
            {
                "name": "GCIL",
                "city": city.id,
                "description": "Lover max guttastemning",
                "contact_email": "styret@gc.no",
            },
            format="json",
        )
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_query_param_non_existing_city(self):
        request = self.factory.get("clubs", {"city": "Gotham"})
        view = ClubViewSet.as_view({"get": "list"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 0)
