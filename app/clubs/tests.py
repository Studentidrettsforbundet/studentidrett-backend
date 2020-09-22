from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from clubs.models import Club
from clubs.views import ClubViewSet
from cities.models import City
from cities.views import CityViewSet


# Create your tests here.


class TestClubApi(APITestCase):

    def setUp(self):
        self.name = 'NTNUI'
        self.city = City(name="Trondheim", region="Trondelag")
        self.description = "This is a club for the best of the best!",
        self.contact_email = "captain1@ntnui.com",
        self.pricing = "about half of your yearly income",
        self.register_info = "You'll have to sell your soul, and bake a cake"

        test1 = Club(
            name=self.name,
            city=self.city,
            description="This is a club for the best of the best!",
            contact_email="captain1@ntnui.com",
            pricing="about half of your yearly income",
            register_info="You'll have to sell your soul, and bake a cake"
                    )

        test2 = Club(
            name="BI lions",
            city=self.city,
            description="We just wanna take your money",
            contact_email="cheif@bilions.com",
            pricing="about all of your yearly income",
            register_info="You'll have to buy champagne for the whole club"
        )

        test1.save()
        test2.save()
        self.factory = APIRequestFactory()

    def test_club_model(self):
        club = Club.objects.all()[0]
        self.assertEqual(club.name, self.name)
        self.assertEqual(club.city, self.city)
        self.assertEqual(club.description, self.description)
        self.assertEqual(club.contact_email, self.contact_email)
        self.assertEqual(club.pricing, self.pricing)
        self.assertEqual(club.register_info, self.register_info)

    def test_clubs_list(self):
        request = self.factory.get('/clubs/')
        view = ClubViewSet.as_view({'get': 'list'})
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check pagination
        self.assertEqual(response.data.keys(), {'count', 'next', 'previous', 'results'})
        # Check fields in result
        self.assertEqual(response.data.get('results')[0].keys(), {'id', 'city', 'name', 'description',
                                                                  'contact_email',
                                                                  'pricing', 'register_info'})

    def test_club_detail(self):
        request = self.factory.get('/clubs/')
        view = ClubViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk='1')
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check fields in result
        self.assertEqual(response.data.keys(),
                         {'id', 'city', 'name', 'description', 'contact_email', 'pricing',
                          'register_info'})

    def test_club_detail_non_existing(self):
        request = self.factory.get('clubs')
        view = ClubViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk='999')
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
