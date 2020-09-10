from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from .models import Interest
from .views import InterestViewSet
from clubs.models import Club


# Create your tests here.


class TestInterestApi(APITestCase):

    def setUp(self):
        club = Club(name="NTNUI")
        club.save()
        user = User.objects.create_superuser('testuser', email='testuser@test.com', password='testing')
        user.save()
        interest = Interest(email='test@test.no', sport='test', club=club)
        interest.save()

        self.factory = APIRequestFactory()
        self.interests = Interest.objects.all()
        self.user = User.objects.get(username='testuser')
        self.post_view = InterestViewSet.as_view({'post': 'create'})
        self.get_list_view = InterestViewSet.as_view({'get': 'list'})
        self.get_detail_view = InterestViewSet.as_view({'get': 'retrieve'})

    def test_post_interests(self):
        request = self.factory.post('/interest/', {'email': 'test@test.no', 'sport': 'football', 'club': 1}, format='json')
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.keys(), {'id', 'email', 'sport', 'club'})

    def test_post_wrong_email(self):
        request = self.factory.post('/interest/', {'email': 'test', 'sport': 'football', 'club': 1}, format='json')
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {'email'})

    def test_post_empty_email(self):
        request = self.factory.post('/interest/', {'email': '', 'sport': 'football', 'club': 1}, format='json')
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {'email'})

    def test_post_empty_sport(self):
        request = self.factory.post('/interest/', {'email': 'test@test.no', 'sport': '', 'club': 1}, format='json')
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {'sport'})

    def test_post_empty_club(self):
        request = self.factory.post('/interest/', {'email': 'test@test.no', 'sport': 'test', 'club': None}, format='json')
        response = self.post_view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {'club'})

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
        self.assertEqual(response.data.keys(), {'id', 'email', 'sport', 'club'})

    def test_get_non_existing_interest(self):
        request = self.factory.get('/interest/')
        force_authenticate(request, self.user)
        response = self.get_detail_view(request, pk=999)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
