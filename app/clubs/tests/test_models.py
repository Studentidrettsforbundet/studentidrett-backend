import pytest
import factory

from cities.models import City
from clubs.models import Club
from clubs.serializers import ClubSerializer
from clubs.views import ClubViewSet
from clubs.factories.club_factories import ClubFactory


class TestClubsModel:

    def test_club_model(self):
        