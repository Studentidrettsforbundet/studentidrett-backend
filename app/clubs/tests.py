from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from clubs.models import Club
from clubs.views import ClubViewSet


# Create your tests here.


class TestClubsApi(APITestCase):

    def setUp(self):
        club = Club(name="NTNUI")
        club.save()
        self.factory = APIRequestFactory()

    def test_clubs_list(self):
        request = self.factory.get('clubs')
        view = ClubViewSet.as_view({'get': 'list'})
        response = view(request)
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check pagination
        self.assertEqual(response.data.keys(), {'count', 'next', 'previous', 'results'})
        # Check fields in result
        self.assertEqual(response.data.get('results')[0].keys(), {'id', 'city', 'name', 'information',
                                                                  'contact_email', 'contact_phone',
                                                                  'pricing', 'register_info'})

    def test_club_detail(self):
        request = self.factory.get('clubs')
        view = ClubViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk='1')
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check fields in result
        self.assertEqual(response.data.keys(),
                         {'id', 'city', 'name', 'information', 'contact_email', 'contact_phone', 'pricing',
                          'register_info'})

    def test_club_detail_non_existing(self):
        request = self.factory.get('clubs')
        view = ClubViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk='999')
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
