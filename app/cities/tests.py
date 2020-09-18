from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from .models import City
from .views import CityViewSet


# Create your tests here.


class TestCityApi(APITestCase):

    def setUp(self):
        city = City(name="Trondheim", region="midt")
        city.save()
        self.factory = APIRequestFactory()
        self.cities = City.objects.all()

    def test_cities_list(self):
        request = self.factory.get('cities/')
        view = CityViewSet.as_view({'get': 'list'})
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check pagination
        self.assertEqual(response.data.keys(), {'count', 'next', 'previous', 'results'})
        # Check fields in result
        self.assertEqual(response.data.get('results')[0].keys(), {'id', 'name', 'region', 'clubs'})

    def test_city_detail(self):
        request = self.factory.get('cities')
        view = CityViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk='1')
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check fields in result
        self.assertEqual(response.data.keys(), {'id', 'name', 'region', 'clubs'})

    def test_city_detail_non_existing(self):
        request = self.factory.get('cities')
        view = CityViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk='999')
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_city_post_not_allowed(self):
        request = self.factory.post('cities', {'name': 'Oslo', 'region': 'øst'})
        view = CityViewSet.as_view({'post': 'post'})
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_query_param_region(self):
        city = City(name="Stjørdal", region="midt")
        city.save()
        request = self.factory.get('cities', {'region': 'midt'})
        view = CityViewSet.as_view({'get': 'list'})
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check length of results
        self.assertEqual(len(response.data.get('results')), 2)
        # Check that both clubs are in Trondheim
        self.assertEqual(response.data.get('results')[0].get('name'), 'Trondheim')
        self.assertEqual(response.data.get('results')[1].get('name'), 'Stjørdal')


    def test_query_param_non_existing_region(self):
        request = self.factory.get('cities', {'region': 'fest'})
        view = CityViewSet.as_view({'get': 'list'})
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_query_param_no_cities_in_region(self):
        request = self.factory.get('cities', {'region': 'vest'})
        view = CityViewSet.as_view({'get': 'list'})
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check length of results
        self.assertEqual(len(response.data.get('results')), 0)
