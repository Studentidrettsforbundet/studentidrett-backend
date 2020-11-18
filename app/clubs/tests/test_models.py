import django.db.utils

import pytest
from rest_framework.test import APITestCase

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
