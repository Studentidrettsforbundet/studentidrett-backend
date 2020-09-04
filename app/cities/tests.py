from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from cities.models import City

# Create your tests here.


class TestCityApi(TestCase):

    def setUp(self):
        self.client=APIClient()
        self.cities=City.objects.all()

    def test_get_all_cities(self):
        response=self.client.get('cities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), )
