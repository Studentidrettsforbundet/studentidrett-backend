import factory

from teams.models import Team


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = "NTNUI fotball"
