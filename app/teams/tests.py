from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import json


from .models import Team
from groups.models import Group
from .serializers import TeamSerializer
from clubs.models import Club

# initialize the APIClient app
client = APIClient()


# Create your tests here.


class TeamModelTest(TestCase):
    def setUp(self):

        self.club = Club.objects.create(name="TestClub")
        self.group = Group.objects.create(name="TestGroup", club=self.club)

        Team.objects.create(
            name='TeamName1',
            full_capacity=True,
            tryouts=True,
            registration_open=False,
            group=self.group)

    def test_team_attributes(self):
        team = Team.objects.get(name='TeamName1')
        self.assertEqual(team.name, 'TeamName1')
        self.assertEqual(team.full_capacity, True)
        self.assertEqual(team.tryouts, True)
        self.assertEqual(team.registration_open, False)
        self.assertEqual(team.group, self.group)


class TeamViewTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name="TestClub")
        self.group = Group.objects.create(name="TestGroup", club=self.club)
        Team.objects.create(
            name='TeamName1',
            full_capacity=True,
            tryouts=True,
            registration_open=False,
            group=self.group)
        Team.objects.create(
            name='TeamName2',
            full_capacity=False,
            tryouts=True,
            registration_open=True,
            group=self.group)
        Team.objects.create(
            name='TeamName3',
            full_capacity=False,
            tryouts=False,
            registration_open=True,
            group=self.group)

    def test_team_contains_expected_fields(self):
        response = client.get('/teams/1/')
        self.assertEqual(response.data.keys(), {'id', 'name', 'full_capacity', 'tryouts', 'registration_open', 'group'})

    def test_team_detail(self):
        response = client.get('/teams/2/')
        self.assertEqual(json.loads(response.content),
                         {'id': 2,
                          'name': 'TeamName2',
                          'full_capacity': False,
                          'tryouts': True,
                          'registration_open': True,
                          'group': self.group.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_list(self):
        # get API response
        response = client.get('/teams/')
        # get data from db
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_team(self):
        club = Club.objects.create(name="TestClub")
        group = Group.objects.create(name="TestGroup2", club=club)
        response = self.client.post('/teams/', {
            "id": 5,
            "name": "post",
            "full_capacity": False,
            "tryouts": True,
            "registration_open": True,
            "group": group.id},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Team.objects.filter(name="post").exists())

    def test_get_nonexistent_team(self):
        response = client.get('/teams/42/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)