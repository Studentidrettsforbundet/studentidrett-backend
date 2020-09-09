from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from .models import City
from .views import CityViewSet


# Create your tests here.


class TestCityApi(APITestCase):

    def setUp(self):
        city = City(name="Trondheim", region="Trondelag")
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
