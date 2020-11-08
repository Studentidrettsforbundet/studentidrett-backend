from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from cities.models import City
from cities.serializers import CitySerializer
from cities.views import CityViewSet

from cities.factories.city_factories import CityFactoryT, CityFactoryB


def get_response(request, user=None, city_id=None):
    """
    Converts a request to a response.
    :param request: the desired HTTP-request.
    :param user: the user performing the request. None represents an anonymous user
    :param city_id: the desired city. None represents all cities.
    :return: the HTTP-response from Django.
    """

    force_authenticate(request, user=user)
    if city_id:
        view = CityViewSet.as_view({"get": "retrieve"})
        return view(request, pk=city_id)
    else:
        view = CityViewSet.as_view({"get": "list"})
        return view(request)


class TestCityApi(TestCase):
    def setUp(self):
        self.city1 = CityFactoryT()
        self.city2 = CityFactoryB()
        self.factory = APIRequestFactory()
        self.cities = City.objects.all()

    def test_city_detail(self):
        request = self.factory.get("/cities/")
        response = get_response(request, city_id=self.city1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CitySerializer(self.city1).data)

    def test_cities_list(self):
        request = self.factory.get("/cities/")
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {"count", "next", "previous", "results"})
        self.assertEqual(len(response.data.get("results")), len(self.cities))
        self.assertEqual(
            response.data.get("results"), CitySerializer(self.cities, many=True).data
        )

    def test_city_detail_non_existing(self):
        request = self.factory.get("cities")
        response = get_response(request, city_id="99")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_param_region(self):
        request = self.factory.get("cities", {"region": "midt"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
        self.assertEqual(
            response.data.get("results")[0], CitySerializer(self.city1).data
        )

    def test_query_param_non_existing_region(self):
        request = self.factory.get("cities", {"region": "fest"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_param_no_cities_in_region(self):
        request = self.factory.get("cities", {"region": "nord"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 0)
