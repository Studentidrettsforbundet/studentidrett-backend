from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
import json

from .models import Group
from .views import GroupViewSet
from .serializers import GroupSerializer

from sports.models import Sport
from clubs.models import Club
from cities.models import City


#initialize the APIClient app
client = APIClient()
# Create your tests here.


class GroupsModelTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name="TestClub")
        self.sport = Sport.objects.create(name="TestSport")
        self.city = City.objects.create(name="TestCity")

        Group.objects.create(
            name='Group1',
            description = 'This is a description',
            cover_photo =  None,
            sport_type = self.sport,
            club = self.club,
            city = self.city
        )

    def test_group_attributes(self):
        group = Group.objects.get(name='Group1')
        self.assertEqual(group.name, 'Group1')
        self.assertEqual(group.description, 'This is a description')
        self.assertFalse(group.cover_photo is None) #TODO fix this test
        self.assertEqual(group.sport_type, self.sport)
        self.assertEqual(group.club, self.club)
        self.assertEqual(group.city, self.city)



class GroupViewTest(TestCase):
    def setUp(self):
        club = Club(name="TestClub")
        club.save()

        sport = Sport(name="TestSport")
        sport.save()

        city = City(name="TestCity")
        city.save()

        user = User.objects.create_superuser(username='testuser',  email='testuser@test.com', password='testing')

        self.factory = APIRequestFactory()
        self.group = Group.objects.all()
        self.user = User.objects.get(username='testuser')
        self.post_view = GroupViewSet.as_view({'post': 'create'})
        self.get_list_view = GroupViewSet.as_view({'get': 'list'})
        self.get_detail_view = GroupViewSet.as_view({'get': 'retrieve'})


    def test_post_groups(self):
        request = self.factory.post('/groups/', {
              'name' :'Group1',
              'description': 'This is a description',
              'cover_photo': None,
              'sport_type' : self.sport,
              'club' : self.club,
              'city': self.city
             }, format = 'json')
        #bytte til city.id eller bare 1
        force_authenticate(request, self.user)
        response = self.post_view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        '''Group.objects.create(
            name='Group1',
            description='This is a description',
            cover_photo=None,
            sport_type= ,
            club=self.club,
            city = self.city
        )

        Group.objects.create(
            name='Group2',
            description='This is a description',
            cover_photo=None,
            sport_type=self.sport,
            club=self.club,
            city=self.city

        )

        Group.objects.create(
            name='Group3',
            description='This is a description',
            cover_photo=None,
            sport_type=self.sport,
            club=self.club,
            city=self.city

        )'''

    def test_group_contains_expected_fields(self):
        request = self.factory.get('/groups/')
        force_authenticate(request, self.user)
        response = self.get_detail_view(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {'id', 'name', 'description', 'cover_photo',
                                                'sport_type', 'club', 'city'})


    def test_group_detail(self):
        request = self.factory.get('/groups/')
        force_authenticate(request, self.user)
        response = self.get_detail_view(request, pk=1)

        self.assertEqual(json.loads(response.content),
                         {'id':1,
                          'name' :'Group1',
                          'description': 'This is a description',
                          'cover_photo': None,
                          'sport_type' : self.sport.id,
                          'club' : self.club.id,
                          'city': self.city.id
                         })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_group_list(self):
        request = self.factory.get('/groups/')
        force_authenticate(request, self.user)
        response = self.get_list_view(request)

        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)

        #Check pagination
        self.assertEqual(response.data.keys(), {'count', 'next', 'previous', 'results'})
        #Check if object in response correlates with objects in database
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_group(self):
        club = Club.objects.create(name="Club")
        sport = Sport.objects.create(name = "Sport")
        city = City.objects.create(name="City")

        request = self.factory.post('/groups/', {
                                    'name': 'Group4',
                                    'description': 'This is a description',
                                    'cover_photo': '',
                                    'sport_type': sport.id,
                                    'club': club.id,
                                    'city': city.id
                                    },
                                    format='json')

        force_authenticate(request, self.user)
        response = self.post_view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Group.objects.filter(name='Group4').exists())

    def test_get_nonexistent_group(self):
        request = self.factory.get('/groups/69/')
        force_authenticate(request, self.user)
        response = self.get_detail_view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_groups_auth(self):
        request = self.factory.get('/groups/')
        response = self.get_list_view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_group_auth(self):
        request = self.factory.post('/groups/', {
                                            'id': 5,
                                            'name': 'Group4',
                                            'description': 'This is a description',
                                            'cover_photo': '',
                                            'sport_type': self.sport,
                                            'club': self.club,
                                            'city': self.city
                                            },
                                            format='json')
        response = self.post_view(request)
        self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)
