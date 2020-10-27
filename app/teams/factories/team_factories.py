import factory

from teams.models import Team

from cities.factories.city_factories import CityFactory


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = "NTNUI fotball"
