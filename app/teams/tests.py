from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from cities.models import City
from clubs.models import Club
from groups.models import Group
from sports.models import Sport
from teams.models import Team
from teams.serializers import TeamSerializer
from teams.views import TeamViewSet

from django.contrib.auth.models import User

# initialize the APIClient app
client = APIClient()
factory = APIRequestFactory()


# Create your tests here.


class TestTeam(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(
            "testuser", email="testuser@test.com", password="testing"
        )
        user.save()

        self.user = User.objects.get(username="testuser")
        self.city = City.objects.create(name="Trondelag")
        self.club = Club.objects.create(name="TestClub")
        self.group = Group.objects.create(name="TestGroup", club=self.club)
        self.sport = Sport.objects.create(name="Fotball")

        Team.objects.create(
            name="test",
            location=self.city,
            group=self.group,
            sport=self.sport,
            description="Dette er et lag",
            cost="1000kr i uka",
            equipment="Susp, baller av stål og en teskje",
            gender="M",
            skill_level="LOW",
            season="Høst til vår",
            facebook_link="facebook.com",
            availability="OP",
        )
        Team.objects.create(
            name="test2",
            location=self.city,
            group=self.group,
            sport=self.sport,
            description="Dette er enda et lag",
            cost="1000kr i uka",
            equipment="Susp, baller av stål og en teskje",
            gender="M",
            skill_level="LOW",
            season="Høst til vår",
            facebook_link="facebook.com",
            availability="OP",
        )

    def test_team_model(self):
        team = Team.objects.all()[0]
        self.assertEqual(team.location, self.city)
        self.assertEqual(team.group, self.group)
        self.assertEqual(team.sport, self.sport)
        self.assertEqual(team.description, "Dette er et lag")
        self.assertEqual(team.cost, "1000kr i uka")
        self.assertEqual(team.equipment, "Susp, baller av stål og en teskje")
        self.assertEqual(team.gender, "M")
        self.assertEqual(team.skill_level, "LOW")
        self.assertEqual(team.season, "Høst til vår")
        self.assertEqual(team.facebook_link, "facebook.com")
        self.assertEqual(team.availability, "OP")

    def test_contains_expected_fields(self):
        request = factory.get("team")
        view = TeamViewSet.as_view({"get": "retrieve"})
        response = view(request, pk="1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.keys(),
            {
                "id",
                "name",
                "location",
                "group",
                "sport",
                "description",
                "cost",
                "equipment",
                "gender",
                "skill_level",
                "season",
                "schedule",
                "tryout_dates",
                "facebook_link",
                "instagram_link",
                "webpage",
                "availability",
                "image",
            },
        )
        team = Team.objects.all()[0]
        serializer = TeamSerializer(team)
        self.assertEqual(response.data, serializer.data)

    def test_team_list(self):
        # get API response
        response = client.get("/teams/")
        # get data from db
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        self.assertEqual(response.data.get("results"), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_team_auth(self):
        request = factory.post(
            "/team/",
            {
                "name": "post",
                "group": self.group.id,
                "sport": self.sport.id,
                "schedule": [],
                "tryout_dates": [],
            },
            format="json",
        )
        force_authenticate(request, self.user)
        view = TeamViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Team.objects.filter(name="post").exists())

    def test_create_new_team_no_auth(self):
        request = factory.post(
            "/team/",
            {
                "name": "post",
                "group": self.group.id,
                "sport": self.sport.id,
                "schedule": [],
                "tryout_dates": [],
            },
            format="json",
        )
        view = TeamViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_team_bad_group(self):
        request = factory.post(
            "/team/",
            {
                "name": "post",
                "group": None,
                "sport": self.sport.id,
                "schedule": [],
                "tryout_dates": [],
            },
            format="json",
        )
        force_authenticate(request, self.user)
        view = TeamViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {"group"})

    def test_create_new_team_bad_sport(self):
        request = factory.post(
            "/team/",
            {
                "name": "post",
                "group": self.group.id,
                "sport": None,
                "schedule": [],
                "tryout_dates": [],
            },
            format="json",
        )
        force_authenticate(request, self.user)
        view = TeamViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {"sport"})

    def test_create_new_team_empty_name(self):
        request = factory.post(
            "/team/",
            {
                "name": "",
                "group": self.group.id,
                "sport": self.sport.id,
                "schedule": [],
                "tryout_dates": [],
            },
            format="json",
        )
        force_authenticate(request, self.user)
        view = TeamViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {"name"})

    def test_create_new_team_bad_name(self):
        request = factory.post(
            "/team/",
            {
                "name": None,
                "group": self.group.id,
                "sport": self.sport.id,
                "schedule": [],
                "tryout_dates": [],
            },
            format="json",
        )
        force_authenticate(request, self.user)
        view = TeamViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {"name"})

    def test_get_non_existing_team(self):
        response = client.get("/team/42/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
