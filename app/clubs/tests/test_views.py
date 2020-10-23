from rest_framework.test import APIRequestFactory, APITestCase


from cities.models import City
from clubs.models import Club
from clubs.serializers import ClubSerializer
from clubs.views import ClubViewSet
from clubs.factories.club_factories import ClubFactory, LongNameClubFactory

