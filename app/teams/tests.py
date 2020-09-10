from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import json


from .models import Team
from clubSports.models import ClubSport
from .serializers import TeamSerializer
from clubs.models import Club

# initialize the APIClient app
client = APIClient()


# Create your tests here.


class TeamModelTest(TestCase):
    def setUp(self):

        self.club = Club.objects.create(name="TestClub")
        self.clubSport = ClubSport.objects.create(name="TestClubSport", club=self.club)

        Team.objects.create(
            name='TeamName1',
            full_capacity=True,
            tryouts=True,
            registration_open=False,
            club_sport=self.clubSport)

    def test_team_attributes(self):
        team = Team.objects.get(name='TeamName1')
        self.assertEqual(team.name, 'TeamName1')
        self.assertEqual(team.full_capacity, True)
        self.assertEqual(team.tryouts, True)
        self.assertEqual(team.registration_open, False)
        self.assertEqual(team.club_sport, self.clubSport)


class TeamViewTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name="TestClub")
        self.clubSport = ClubSport.objects.create(name="TestClubSport", club=self.club)
        Team.objects.create(
            name='TeamName1',
            full_capacity=True,
            tryouts=True,
            registration_open=False,
            club_sport=self.clubSport)
        Team.objects.create(
            name='TeamName2',
            full_capacity=False,
            tryouts=True,
            registration_open=True,
            club_sport=self.clubSport)
        Team.objects.create(
            name='TeamName3',
            full_capacity=False,
            tryouts=False,
            registration_open=True,
            club_sport=self.clubSport)

    def test_contains_expected_fields(self):
        response = client.get('/team/1/')
        self.assertCountEqual(response.data.keys(), {'id', 'name', 'full_capacity', 'tryouts', 'registration_open', 'club_sport'})

    def test_team_detail(self):
        response = client.get('/team/2/')
        self.assertEqual(json.loads(response.content),
                         {'id': 2,
                          'name': 'TeamName2',
                          'full_capacity': False,
                          'tryouts': True,
                          'registration_open': True,
                          'club_sport': self.clubSport.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_list(self):
        # get API response
        response = client.get('/team/')
        # get data from db
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_team(self):
        club = Club.objects.create(name="TestClub")
        clubSport = ClubSport.objects.create(name="TestClubSport2", club=club)
        response = self.client.post('/team/', {
            "id": 5,
            "name": "post",
            "full_capacity": False,
            "tryouts": True,
            "registration_open": True,
            "club_sport": clubSport.id},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Team.objects.filter(name="post").exists())

    def test_get_non_existing_team(self):
        response = client.get('/team/42/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)