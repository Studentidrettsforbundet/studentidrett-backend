from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from cities.models import City
from clubs.models import Club
from groups.models import Group
from groups.serializers import GroupSerializer
from groups.views import GroupViewSet
from sports.models import Sport

from django.contrib.auth.models import User


def get_response(request, user=None, group_id=None):
    """
    Converts a request to a response.
    :param request: the desired HTTP-request.
    :param user: the user performing the request. None represents an anonymous user
    :param group_id: the desired group. None represents all groups.
    :return: the HTTP-response from Django.
    """

    force_authenticate(request, user=user)

    if group_id:
        view = GroupViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        )
        return view(request, pk=group_id)
    else:
        view = GroupViewSet.as_view(
            {"get": "list", "put": "update", "delete": "destroy", "post": "create"}
        )
        return view(request)


class GroupsModelTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name="TestClub")
        self.sport = Sport.objects.create(name="TestSport")
        self.city = City.objects.create(name="TestCity")

        group = Group.objects.create(
            name="Group1",
            description="This is a description",
            cover_photo=None,
            club=self.club,
            city=self.city,
        )
        group.sports.add(self.sport)
        group.save()

    def test_group_attributes(self):
        group = Group.objects.get(name="Group1")

        self.assertEqual(group.name, "Group1")
        self.assertEqual(group.description, "This is a description")
        self.assertFalse(group.cover_photo is None)  # TODO fix this test
        self.assertEqual(list(group.sports.all()), [self.sport])
        self.assertEqual(group.club, self.club)
        self.assertEqual(group.contact_email, None)
        self.assertEqual(group.city, self.city)

    def test_no_duplicate_sports(self):
        group = Group.objects.get(name="Group1")

        self.assertEqual(len(group.sports.all()), 1)

        group.sports.add(self.sport)
        group.save()

        # Same sport-object should not be added again
        self.assertEqual(len(group.sports.all()), 1)

    def test_multiple_sports(self):
        group = Group.objects.get(name="Group1")

        sport = Sport.objects.create(name="Sport2")
        group.sports.add(sport)
        group.save()

        self.assertTrue(len(group.sports.all()), not 1)


class GroupViewTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name="TestClub")
        self.sport = Sport.objects.create(name="TestSport")
        self.city = City.objects.create(name="TestCity")
        self.user = User.objects.create_superuser(
            username="testuser", email="testuser@test.com", password="testing"
        )
        self.group = Group.objects.create(
            name="Group1",
            description="This is a description",
            cover_photo=None,
            club=self.club,
            city=self.city,
        )
        Group.objects.create(
            name="Group2",
            description="This is also a description",
            cover_photo=None,
            club=self.club,
            city=self.city,
        )
        self.group.sports.add(self.sport)
        self.groups = Group.objects.all()
        self.factory = APIRequestFactory()

    def test_group_contains_expected_fields(self):
        request = self.factory.get("/groups/")
        force_authenticate(request, self.user)
        response = get_response(request, group_id=self.group.pk)

        self.assertEqual(
            response.data.keys(),
            {
                "id",
                "name",
                "description",
                "cover_photo",
                "sports",
                "club",
                "city",
                "contact_email",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_group_detail(self):
        request = self.factory.get("/groups/")
        response = get_response(request, group_id=self.group.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, GroupSerializer(self.group).data)

    def test_group_list(self):
        request = self.factory.get("/groups/")
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {"count", "next", "previous", "results"})
        self.assertEqual(len(response.data.get("results")), len(self.groups))
        self.assertEqual(
            response.data.get("results"), GroupSerializer(self.groups, many=True).data
        )

    def test_get_nonexistent_group(self):
        request = self.factory.get("/groups/")
        response = get_response(request, group_id="99")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_group(self):
        request = self.factory.post(
            "/groups/",
            {
                "name": "Group2",
                "description": "This is a description",
                "cover_photo": None,
                "sports": [self.sport.id],
                "club": self.club.id,
                "city": self.city.id,
            },
            format="json",
        )
        response = get_response(request, user=self.user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Group.objects.filter(name="Group2").exists())

    def test_post_group_auth(self):
        request = self.factory.post(
            "/groups/",
            {
                "name": "Group4",
                "description": "This is a description",
                "cover_photo": None,
                "sports": self.sport.id,
                "club": self.club.id,
                "city": self.city.id,
            },
            format="json",
        )
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Group.objects.filter(name="Group4").exists())
