import json

from django.contrib.auth.models import User
from cities.models import City
from clubSports.models import ClubSport
from clubs.models import Club
from sports.models import Sport
from teams.views import TeamViewSet
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate, APIRequestFactory

from .models import Team
from .serializers import TeamSerializer

# initialize the APIClient app
client = APIClient()
factory = APIRequestFactory()


# Create your tests here.


class TestTeam(TestCase):
    def setUp(self):
        user = User.objects.create_superuser('testuser', email='testuser@test.com', password='testing')
        user.save()

        self.user = User.objects.get(username='testuser')
        self.city = City.objects.create(name="Trondelag")
        self.club = Club.objects.create(name="TestClub")
        self.group = ClubSport.objects.create(name="TestClubSport", club=self.club)
        self.sport = Sport.objects.create(name="Fotball")

        Team.objects.create(
            name="test",
            location=self.city,
            group=self.group,
            sport=self.sport,
            description="Dette er et lag",
            schedule=None,
            cost="1000kr i uka",
            equipment="Susp, baller av stål og en teskje",
            gender="Male",
            skill_level="Low",
            season="Høst til vår",
            facebook_link="facebook.com",
            tryuot_dates="Mandag 15.desember",
            availability="Open",
            image=None
        )
        Team.objects.create(
            name="test2",
            location=self.city,
            group=self.clubSport,
            sport=self.sport,
            description="Dette er enda et lag",
            schedule=None,
            cost="1000kr i uka",
            equipment="Susp, baller av stål og en teskje",
            gender="Male",
            skill_level="Low",
            season="Høst til vår",
            facebook_link="facebook.com",
            tryuot_dates="Mandag 15.desember",
            availability="Open",
            image=None
        )

    def test_team_model(self):
        team = Team.objects.get(id='1')
        self.assertEqual(team.location, self.city)
        self.assertEqual(team.group, self.clubSport)
        self.assertEqual(team.sport, self.sport)
        self.assertEqual(team.description, "Dette er et lag")
        self.assertEqual(team.schedule, None)
        self.assertEqual(team.cost, "1000kr i uka")
        self.assertEqual(team.equipment, "Susp, baller av stål og en teskje")
        self.assertEqual(team.gender, "Male")
        self.assertEqual(team.skill_level, "Low")
        self.assertEqual(team.season, "Høst til vår")
        self.assertEqual(team.facebook_link, "facebook.com")
        self.assertEqual(team.tryuot_dates, "Mandag 15.desember")
        self.assertEqual(team.availability, "Open")
        self.assertEqual(team.image, None)

    def test_contains_expected_fields(self):
        response = client.get('/team/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(),
                              {'id', 'name', 'name', 'location', 'group', 'sport', 'description', 'schedule', 'cost',
                               'equipment', 'gender', 'skill_level', 'season', 'facebook_link', 'instagram_link','webpage',
                               'tryout_dates', 'availability', 'image'})

    def test_team_detail(self):
        response = client.get('/team/2/')
        team = Team.objects.get(id='2')
        serializer = TeamSerializer(team)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_team_list(self):
        # get API response
        response = client.get('/team/')
        # get data from db
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_team_auth(self):
        request = factory.post('/team/', {
            "name": "post",
            "location": self.city.id,
            "group": self.group.id,
            "sport": self.sport.id,

        }, format='json')
        force_authenticate(request, self.user)
        view = TeamViewSet.as_view({'post':'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Team.objects.filter(name="post").exists())

    def test_create_new_team_no_auth(self):
        request = factory.post('/team/', {
            "name": "post",
            "location": self.city.id,
            "group": self.group.id,
            "sport": self.sport.id,

        }, format='json')
        view = TeamViewSet.as_view({'post':'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_team_bad_location(self):
        request = factory.post('/team/', {
            "name": "post",
            "location": None,
            "group": self.group.id,
            "sport": self.sport.id,

        }, format='json')
        force_authenticate(request, self.user)
        view = TeamViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {'location'})

    def test_create_new_team_bad_group(self):
        request = factory.post('/team/', {
            "name": "post",
            "location": self.city.id,
            "group": None,
            "sport": self.sport.id,

        }, format='json')
        force_authenticate(request, self.user)
        view = TeamViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {'group'})

    def test_create_new_team_bad_sport(self):
        request = factory.post('/team/', {
            "name": "post",
            "location": self.city.id,
            "group": self.group.id,
            "sport": None,

        }, format='json')
        force_authenticate(request, self.user)
        view = TeamViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {'sport'})

    def test_create_new_team_empty_name(self):
        request = factory.post('/team/', {
            "name": "",
            "location": self.city.id,
            "group": self.group.id,
            "sport": self.sport.id,

        }, format='json')
        force_authenticate(request, self.user)
        view = TeamViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {'name'})

    def test_create_new_team_bad_name(self):
        request = factory.post('/team/', {
            "name": None,
            "location": self.city.id,
            "group": self.group.id,
            "sport": self.sport.id,

        }, format='json')
        force_authenticate(request, self.user)
        view = TeamViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {'name'})

    def test_get_non_existing_team(self):
        response = client.get('/team/42/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
