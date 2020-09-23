from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from clubs.models import Club
from clubs.views import ClubViewSet
from cities.models import City


# Create your tests here.


class TestClubsApi(APITestCase):

    def setUp(self):

        self.name = 'NTNUI'
        self.city1 = City.objects.create(name="Trondheim", region="Trondelag")
        self.city2 = City.objects.create(name="Eiksmarka", region="Baerum")
        self.description = "This is a club for the best of the best!"
        self.contact_email = "captain1@ntnui.com"
        self.pricing = "about half of your yearly income"
        self.register_info = "You'll have to sell your soul, and bake a cake"

        Club.objects.create(
            name=self.name,
            city=self.city1,
            description="This is a club for the best of the best!",
            contact_email="captain1@ntnui.com",
            pricing="about half of your yearly income",
            register_info="You'll have to sell your soul, and bake a cake"
                    )

        Club.objects.create(
            name="BI lions",
            city=self.city2,
            description="We just wanna take your money",
            contact_email="cheif@bilions.com",
            pricing="about all of your yearly income",
            register_info="You'll have to buy champagne for the whole club"
        )
        self.factory = APIRequestFactory()

    def test_club_model(self):
        clubs = Club.objects.all()[1]
        self.assertEqual(clubs.name, self.name)
        self.assertEqual(clubs.city, self.city1)
        self.assertEqual(clubs.description, self.description)
        self.assertEqual(clubs.contact_email, self.contact_email)
        self.assertEqual(clubs.pricing, self.pricing)
        self.assertEqual(clubs.register_info, self.register_info)

    def test_clubs_list(self):
        request = self.factory.get('/clubs/')
        view = ClubViewSet.as_view({'get': 'list'})
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check pagination
        self.assertEqual(response.data.keys(), {'count', 'next', 'previous', 'results'})
        # Check fields in result
        self.assertEqual(response.data.get('results')[1].keys(), {'id', 'city', 'name', 'description',
                                                                  'contact_email',
                                                                  'pricing', 'register_info'})
        # Check length of results
        self.assertEqual(len(response.data.get('results')), 2)

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

    def test_query_param_city(self):
        request = self.factory.get('clubs', {'city': 'Trondheim'})
        view = ClubViewSet.as_view({'get': 'list'})
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check length of results
        self.assertEqual(len(response.data.get('results')), 1)
        # Check that both clubs are in Trondheim
        self.assertEqual(response.data.get('results')[0].get('city'), 1)
        # self.assertEqual(response.data.get('results')[1].get('city'), 2)

    def test_query_param_city_no_clubs(self):
        new_city = City(name="Oslo")
        new_city.save()
        request = self.factory.get('clubs', {'city': 'Oslo'})
        view = ClubViewSet.as_view({'get': 'list'})
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check length of results
        self.assertEqual(len(response.data.get('results')), 0)

    def test_create_club(self):
        city = City.objects.create(name="Bergen")
        response = self.client.post('/clubs/', {
            'name': 'GCIL',
            'city': city.id,
            'description': 'Lover max guttastemning',
            'contact_email': 'styret@gc.no'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Club.objects.filter(name='GCIL').exists())

    def test_query_param_non_existing_city(self):
        request = self.factory.get('clubs', {'city': 'Gotham'})
        view = ClubViewSet.as_view({'get': 'list'})
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check length of results
        self.assertEqual(len(response.data.get('results')), 0)
