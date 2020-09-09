from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import json
from django.contrib.auth import get_user_model


from .models import Team
from .serializers import TeamSerializer
from .views import TeamViewSet

# initialize the APIClient app
client = APIClient()


# Create your tests here.


class TeamModelTest(TestCase):
    def setUp(self):

        # sport = ClubSport.object.create(description="desc") temporary before ClubSports is made

        Team.objects.create(
            name='TeamName1',
            full_capacity=True,
            tryouts=True,
            registration_open=False,
            club_sport=1) # change needed when ClubSports is made

    def test_team_attributes(self):
        team = Team.objects.get(name='TeamName1')
        #sport = ClubSport.objects.get(description='desc') temporary removed before ClubSports is made
        self.assertEqual(team.name, 'TeamName1')
        self.assertEqual(team.full_capacity, True)
        self.assertEqual(team.tryouts, True)
        self.assertEqual(team.registration_open, False)
        # self.assertEqual(team.club_sport, sport) temporary before ClubSports is made
        self.assertEqual(team.club_sport, 1)


class TeamViewTest(TestCase):
    def setUp(self):

        Team.objects.create(
            name='TeamName1',
            full_capacity=True,
            tryouts=True,
            registration_open=False,
            club_sport=1)
        Team.objects.create(
            name='TeamName2',
            full_capacity=False,
            tryouts=True,
            registration_open=True,
            club_sport=2)
        Team.objects.create(
            name='TeamName3',
            full_capacity=False,
            tryouts=False,
            registration_open=True,
            club_sport=3)

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
                          'club_sport': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_list(self):
        # get API response
        response = client.get('/team/')
        # get data from db
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_team(self):
        response = self.client.post('/team/', {
            "id": 5,
            "name": "post",
            "full_capacity": False,
            "tryouts": True,
            "registration_open": True,
            "club_sport": 99},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Team.objects.filter(name='post').exists())

    def test_get_non_existing_team(self):
        response = client.get('/team/42/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)