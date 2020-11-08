import factory

from groups.models import Group

from clubs.factories.club_factories import ClubFactory
from sports.factories.sport_factories import SportFactory


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = "NTNUI Turn"
    description = "We are gymnastics"
    contact_email = factory.Faker("email")
