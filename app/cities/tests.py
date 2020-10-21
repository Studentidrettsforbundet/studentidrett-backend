from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from .models import City
from .serializers import CitySerializer
from .views import CityViewSet


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
        self.city = City.objects.create(name="Trondheim", region="midt")
        self.city2 = City.objects.create(name="Bergen", region="vest")
        self.factory = APIRequestFactory()
        self.cities = City.objects.all()
        self.response_format = dict(
            {
                "nord": [],
                "midt": [
                    {
                        "id": self.city.pk,
                        "name": "Trondheim",
                        "region": "midt",
                        "clubs": [],
                    }
                ],
                "vest": [
                    {
                        "id": self.city2.pk,
                        "name": "Bergen",
                        "region": "vest",
                        "clubs": [],
                    }
                ],
                "sor": [],
                "ost": [],
            }
        )

    def test_city_detail(self):
        request = self.factory.get("/cities/")
        response = get_response(request, city_id=self.city.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CitySerializer(self.city).data)

    def test_cities_list(self):
        request = self.factory.get("/cities/")
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), self.response_format.keys())
        self.assertEqual(response.data, self.response_format)

    def test_city_detail_non_existing(self):
        request = self.factory.get("cities")
        response = get_response(request, city_id="99")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_param_region(self):
        request = self.factory.get("cities", {"region": "midt"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["midt"], self.response_format["midt"])

    def test_query_param_non_existing_region(self):
        request = self.factory.get("cities", {"region": "fest"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_param_no_cities_in_region(self):
        request = self.factory.get("cities", {"region": "nord"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["nord"]), 0)
