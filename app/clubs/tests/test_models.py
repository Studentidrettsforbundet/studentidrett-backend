import pytest
import factory.random

import django.db.utils

from rest_framework.test import APIRequestFactory, APITestCase


from cities.models import City
from clubs.models import Club
from clubs.serializers import ClubSerializer
from clubs.views import ClubViewSet
from clubs.factories.club_factories import ClubFactory, LongNameClubFactory


@pytest.mark.django_db
class TestClubsModel(APITestCase):

    def setUp(self):
        self.club = ClubFactory(membership_fee="200kr")

    def test_club_model(self):
        assert self.club.name == "GCIL"
        assert self.club.contact_email == "contact@gcil.com"
        assert self.club.membership_fee == "200kr"

    def test_club_field_lengths(self):
        with pytest.raises(django.db.utils.DataError):
            self.club2 = LongNameClubFactory()





