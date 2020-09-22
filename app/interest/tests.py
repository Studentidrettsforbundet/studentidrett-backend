from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from .models import Interest
from .views import InterestViewSet
from clubs.models import Club
from groups.models import Group


# Create your tests here.


class TestInterestApi(APITestCase):

    def setUp(self):
        club = Club(name="NTNUI")
        club.save()
        group = Group(name="NTNUI Fotball", club=club)
        group.save()
        self.group_id = group.id
        user = User.objects.create_superuser('testuser', email='testuser@test.com', password='testing')
        user.save()
        interest = Interest(cookie_key='c00k13M0n5t3r', group=group)
        interest.save()

        self.factory = APIRequestFactory()
        self.interests = Interest.objects.all()
        self.user = User.objects.get(username='testuser')
        self.post_view = InterestViewSet.as_view({'post': 'create'})
        self.get_list_view = InterestViewSet.as_view({'get': 'list'})
        self.get_detail_view = InterestViewSet.as_view({'get': 'retrieve'})

    def test_post_interests(self):
        request = self.factory.post('/interest/', {'cookie_key': 'c00k13M0n5t3r1sN0M0r3', 'group': 1}, format='json')
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.keys(), {'id', 'cookie_key', 'group', 'created'})

    def test_post_used_cookie_key(self):
        request = self.factory.post('/interest/', {'cookie_key': 'c00k13M0n5t3r', 'group': self.group_id}, format='json')
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {'non_field_errors'})

    def test_post_empty_cookie_key(self):
        request = self.factory.post('/interest/', {'cookie_key': '', 'group': 1}, format='json')
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {'cookie_key'})

    def test_post_empty_club(self):
        request = self.factory.post('/interest/', {'cookie_key': 'testetestetest', 'group': None}, format='json')
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {'group'})

    def test_get_interests_no_auth(self):
        request = self.factory.get('/interest/')
        response = self.get_list_view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.keys(), {'detail'})

    def test_get_interests_auth(self):
        request = self.factory.get('/interest/')
        force_authenticate(request, self.user)
        response = self.get_list_view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {'count', 'next', 'previous', 'results'})
        self.assertEqual(len(response.data.get('results')), len(self.interests))

    def test_get_interest_detail_no_auth(self):
        request = self.factory.get('/interest/')
        response = self.get_detail_view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.keys(), {'detail'})

    def test_get_interest_detail_auth(self):
        request = self.factory.get('/interest/')
        force_authenticate(request, self.user)
        response = self.get_detail_view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {'id', 'cookie_key', 'group', 'created'})

    def test_get_non_existing_interest(self):
        request = self.factory.get('/interest/')
        force_authenticate(request, self.user)
        response = self.get_detail_view(request, pk=999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
