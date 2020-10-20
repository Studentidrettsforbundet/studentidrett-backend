from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from cities.models import City
from clubs.models import Club
from groups.models import Group
from sports.models import Sport
from teams.models import Team
from teams.serializers import TeamSerializer
from teams.views import TeamViewSet

from django.contrib.auth.models import User


def get_response(request, user=None, team_id=None):
    """
    Converts a request to a response.
    :param request: the desired HTTP-request.
    :param user: the user performing the request. None represents an anonymous user
    :param team_id: the desired team. None represents all teams.
    :return: the HTTP-response from Django.
    """

    force_authenticate(request, user=user)

    if team_id:
        view = TeamViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        )
        return view(request, pk=team_id)
    else:
        view = TeamViewSet.as_view(
            {"get": "list", "put": "update", "delete": "destroy", "post": "create"}
        )
        return view(request)


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

        self.team = Team.objects.create(
            name="test",
            location=self.city,
            group=self.group,
            sport=self.sport,
            long_description="Dette er et lag",
            short_description="Lag",
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
            long_description="Dette er enda et lag",
            short_description="Lag",
            cost="1000kr i uka",
            equipment="Susp, baller av stål og en teskje",
            gender="M",
            skill_level="LOW",
            season="Høst til vår",
            facebook_link="facebook.com",
            availability="OP",
        )
        self.teams = Team.objects.all()
        self.factory = APIRequestFactory()

    def test_team_detail(self):
        request = self.factory.get("/teams/")
        response = get_response(request, team_id=self.team.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TeamSerializer(self.team).data)

    def test_team_list(self):
        request = self.factory.get("/teams/")
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {"count", "next", "previous", "results"})
        self.assertEqual(len(response.data.get("results")), len(self.teams))
        self.assertEqual(
            response.data.get("results"), TeamSerializer(self.teams, many=True).data
        )

    def test_post_team(self):
        request = self.factory.post(
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
        response = get_response(request, user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Team.objects.filter(name="post").exists())

    def test_post_team_auth(self):
        request = self.factory.post(
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
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_team_bad_group(self):
        request = self.factory.post(
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
        response = get_response(request, user=self.user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {"group"})

    def test_create_new_team_bad_sport(self):
        request = self.factory.post(
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
        response = get_response(request, user=self.user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {"sport"})

    def test_create_new_team_empty_name(self):
        request = self.factory.post(
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
        response = get_response(request, user=self.user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {"name"})

    def test_create_new_team_bad_name(self):
        request = self.factory.post(
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
        response = get_response(request, user=self.user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.keys(), {"name"})

    def test_get_non_existing_team(self):
        request = self.factory.get("/teams/")
        response = get_response(request, team_id="99")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_param_group(self):
        request = self.factory.get("/teams/", {"group": self.group.name})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), len(self.teams))
        self.assertEqual(
            response.data.get("results"), TeamSerializer(self.teams, many=True).data
        )

    def test_query_param_group_no_teams(self):
        request = self.factory.get("/teams/", {"group": "NoTeams"})
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 0)
