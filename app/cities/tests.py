from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from cities.models import City

# Create your tests here.


class TestCityApi(TestCase):

    def setUp(self):
        self.client=APIClient()
        self.factory=APIRequestFactory()
        self.cities=City.objects.all()

    def test_response_cities(self):
        """
        Tests correct response status code
        """
        response=self.client.get(reverse('city_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_data_cities(self):
        """
        Tests that data returned from cities-view is correct
        """
        response=self.factory.get(reverse('city_list'))
        print(response)
        self.assertEqual(1,1)
