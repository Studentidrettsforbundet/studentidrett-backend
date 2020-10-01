from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory

from .models import City
from .views import CityViewSet


class TestCityApi(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Trondheim", region="midt")
        self.factory = APIRequestFactory()
        self.cities = City.objects.all()

    def test_cities_list(self):
        request = self.factory.get("/cities/")
        view = CityViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {"count", "next", "previous", "results"})
        self.assertEqual(
            response.data.get("results")[0].keys(), {"id", "name", "region", "clubs"}
        )

    def test_city_detail(self):
        request = self.factory.get("/cities/")
        view = CityViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.city.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {"id", "name", "region", "clubs"})

    def test_city_detail_non_existing(self):
        request = self.factory.get("cities")
        view = CityViewSet.as_view({"get": "retrieve"})
        response = view(request, pk="999")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_param_region(self):
        city = City(name="Stjørdal", region="midt")
        city.save()
        request = self.factory.get("cities", {"region": "midt"})
        view = CityViewSet.as_view({"get": "list"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 2)
        self.assertEqual(response.data.get("results")[0].get("name"), "Trondheim")
        self.assertEqual(response.data.get("results")[1].get("name"), "Stjørdal")

    def test_query_param_non_existing_region(self):
        request = self.factory.get("cities", {"region": "fest"})
        view = CityViewSet.as_view({"get": "list"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_query_param_no_cities_in_region(self):
        request = self.factory.get("cities", {"region": "vest"})
        view = CityViewSet.as_view({"get": "list"})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 0)
