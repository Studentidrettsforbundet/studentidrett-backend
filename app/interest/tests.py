from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from clubs.models import Club
from groups.models import Group
from interest.models import Interest
from interest.serializers import InterestSerializer
from interest.views import InterestViewSet

from django.contrib.auth.models import User


def get_response(request, user=None, interest_id=None, create=False):
    """
    Converts a request to a response.
    :param request: the desired HTTP-request.
    :param user: the user performing the request. None represents an anonymous user
    :param interest_id: the desired interest. None represents all interests.
    :param create: set if creating a new interest instance.
    :return: the HTTP-response from Django.
    """

    force_authenticate(request, user=user)

    if interest_id:
        view = InterestViewSet.as_view({"get": "retrieve"})
        return view(request, pk=interest_id)
    elif create:
        view = InterestViewSet.as_view({"post": "create"})
        return view(request)
    else:
        view = InterestViewSet.as_view({"get": "list"})
        return view(request)


class TestInterestApi(APITestCase):
    def setUp(self):
        self.club = Club(name="NTNUI")
        self.club.save()
        self.group = Group(name="NTNUI Fotball", club=self.club)
        self.group.save()
        self.user = User.objects.create_superuser(
            "testuser", email="testuser@test.com", password="testing"
        )
        self.user.save()
        self.interest = Interest(session_id="c00k13M0n5t3r", group=self.group)
        self.interest.save()
        self.factory = APIRequestFactory()
        self.interests = Interest.objects.all()

    def test_post_interests(self):
        request = self.factory.post(
            "/interest/",
            {"group": self.group.pk, "session_id": "c00k13"},
            format="json",
            HTTP_ORIGIN="localhost:8000",
        )
        response = get_response(request, create=True)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.keys(), {"id", "session_id", "group", "created"})

    def test_post_used_session_id(self):
        request = self.factory.post(
            "/interest/",
            {"group": self.group.pk, "session_id": "c00k13M0n5t3r"},
            format="json",
            HTTP_ORIGIN="localhost:8000",
        )
        response = get_response(request, create=True)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_empty_session_id(self):
        request = self.factory.post(
            "/interest/",
            {"group": self.group.pk},
            format="json",
            HTTP_ORIGIN="localhost:8000",
        )
        response = get_response(request, create=True)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_empty_club(self):
        request = self.factory.post(
            "/interest/",
            {"session_id": "no_group"},
            format="json",
            HTTP_ORIGIN="localhost:8000",
        )
        response = get_response(request, create=True)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_interests_no_auth(self):
        request = self.factory.get("/interest/")
        response = get_response(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_interests_auth(self):
        request = self.factory.get("/interest/")
        response = get_response(request, user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), {"count", "next", "previous", "results"})
        self.assertEqual(len(response.data.get("results")), len(self.interests))
        self.assertEqual(
            response.data.get("results"),
            InterestSerializer(self.interests, many=True).data,
        )

    def test_get_interest_detail_no_auth(self):
        request = self.factory.get("/interest/")
        response = get_response(request, interest_id=self.interest.pk)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_interest_detail_auth(self):
        request = self.factory.get("/interest/")
        response = get_response(request, user=self.user, interest_id=self.interest.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, InterestSerializer(self.interest).data)

    def test_get_non_existing_interest(self):
        request = self.factory.get("/interest/")
        response = get_response(request, user=self.user, interest_id="99")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
