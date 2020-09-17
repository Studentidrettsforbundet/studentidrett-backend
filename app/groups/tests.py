from django.test import TestCase
from rest_framework import status
from rest_framework.test  import APIClient
import json

from .models import Group
from clubs.models import Club
from .serializers import GroupSerializer

from sports.models import Sport


#initialize the APIClient app
client = APIClient()

# Create your tests here.


class GroupsModelTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name="TestClub")
        self.sport = Sport.objects.create(name="TestSport")

        Group.objects.create(
            name='Group1',
            description = 'This is a description',
            cover_photo =  None,
            sport_type = self.sport,
            club = self.club,
            contact_person = None,
            contact_email = None,
        )

    def test_group_attributes(self):
        group = Group.objects.get(name='Group1')
        self.assertEqual(group.name, 'Group1')
        self.assertEqual(group.description, 'This is a description')
        self.assertFalse(group.cover_photo is None) #TODO fix this test
        self.assertEqual(group.sport_type, self.sport)
        self.assertEqual(group.club, self.club)
        self.assertEqual(group.contact_person, None)
        self.assertEqual(group.contact_email, None)

class GroupViewTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name="TestClub")
        self.sport = Sport.objects.create(name="TestSport")

        Group.objects.create(
            name='Group1',
            description='This is a description',
            cover_photo=None,
            sport_type=self.sport,
            club=self.club,
            contact_person=None,
            contact_email=None,
        )

        Group.objects.create(
            name='Group2',
            description='This is a description',
            cover_photo=None,
            sport_type=self.sport,
            club=self.club,
            contact_person=None,
            contact_email=None,
        )

        Group.objects.create(
            name='Group3',
            description='This is a description',
            cover_photo=None,
            sport_type=self.sport,
            club=self.club,
            contact_person=None,
            contact_email=None,
        )

    def test_group_contains_expected_fields(self):
        response = client.get('/groups/1/')
        self.assertEqual(response.data.keys(), {'id', 'name', 'description', 'cover_photo',
                                                'sport_type', 'club', 'contact_person',
                                                'contact_email'})

    def test_group_detail(self):
        response = client.get('/groups/1/')
        self.assertEqual(json.loads(response.content),
                         {'id':1,
                          'name' :'Group1',
                          'description': 'This is a description',
                          'cover_photo': None,
                          'sport_type' : self.sport.id,
                          'club' : self.club.id,
                          'contact_person' : None,
                          'contact_email' : None
                         })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_group_list(self):
        response = client.get('/groups/')
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

        response = self.client.post('/groups/', {
                                    'id': 5,
                                    'name': 'Group4',
                                    'description': 'This is a description',
                                    #'cover_photo': None,
                                    'sport_type': sport.id,
                                    'club': club.id,
                                    #'contact_person': None,
                                    #'contact_email': None
                                    },
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Group.objects.filter(name='Group4').exists())

    def test_get_nonexistent_group(self):
        response = client.get('/groups/69/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)