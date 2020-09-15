from django.test import TestCase
from rest_framework import status
from rest_framework.test  import APIClient
import json

from .models import ClubSport
from clubs.models import Club
from .serializers import ClubSportSerializer

from sports.models import Sport


#initialize the APIClient app
client = APIClient()

# Create your tests here.


class ClubSportsModelTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name="TestClub")
        self.sport = Sport.objects.create(name="TestSport")

        ClubSport.objects.create(
            name='ClubSport1',
            description = 'This is a description',
            cover_photo =  None,
            sport_type = self.sport,
            club = self.club,
            contact_person = None,
            contact_email = None,
        )

    def test_clubsport_attributes(self):
        clubsport = ClubSport.objects.get(name='ClubSport1')
        self.assertEqual(clubsport.name, 'ClubSport1')
        self.assertEqual(clubsport.description, 'This is a description')
        self.assertFalse(clubsport.cover_photo is None) #TODO fix this test
        self.assertEqual(clubsport.sport_type, self.sport)
        self.assertEqual(clubsport.club, self.club)
        self.assertEqual(clubsport.contact_person, None)
        self.assertEqual(clubsport.contact_email, None)

class ClubSportViewTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name="TestClub")
        self.sport = Sport.objects.create(name="TestSport")

        ClubSport.objects.create(
            name='ClubSport2',
            description='This is a description',
            cover_photo=None,
            sport_type=self.sport,
            club=self.club,
            contact_person=None,
            contact_email=None,
        )

        ClubSport.objects.create(
            name='ClubSport3',
            description='This is a description',
            cover_photo=None,
            sport_type=self.sport,
            club=self.club,
            contact_person=None,
            contact_email=None,
        )

        ClubSport.objects.create(
            name='ClubSport4',
            description='This is a description',
            cover_photo=None,
            sport_type=self.sport,
            club=self.club,
            contact_person=None,
            contact_email=None,
        )

    def test_clubsport_contains_expected_fields(self):
        response = client.get('/clubsports/1/')
        self.assertEqual(response.data.keys(), {'id', 'name', 'description', 'cover_photo',
                                                'sport_type', 'club', 'contact_person',
                                                'contact_email'})

    def test_clubsport_detail(self):
        response = client.get('/clubsports/1/')
        self.assertEqual(json.loads(response.content),
                         {'id':1,
                          'name' :'ClubSport2',
                          'description': 'This is a description',
                          'cover_photo': None,
                          'sport_type' : self.sport.id,
                          'club' : self.club.id,
                          'contact_person' : None,
                          'contact_email' : None
                         })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_clubsport_list(self):
        response = client.get('/clubsports/')
        clubsports = ClubSport.objects.all()
        serializer = ClubSportSerializer(clubsports, many=True)

        #Check pagination
        self.assertEqual(response.data.keys(), {'count', 'next', 'previous', 'results'})
        #Check if object in response correlates with objects in database
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_clubsport(self):
        club = Club.objects.create(name="Club")
        sport = Sport.objects.create(name = "Sport")

        response = self.client.post('/clubsports/', {
                                    'id': 5,
                                    'name': 'ClubSport5',
                                    'description': 'This is a description',
                                    #'cover_photo': None,
                                    'sport_type': sport.id,
                                    'club': club.id,
                                    #'contact_person': None,
                                    #'contact_email': None
                                    },
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ClubSport.objects.filter(name='ClubSport5').exists())

    def test_get_nonexistent_clubsport(self):
        response = client.get('/clubsports/69/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)