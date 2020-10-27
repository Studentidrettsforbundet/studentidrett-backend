import factory

from sports.models import Sport


class SportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sport

    name = "Turn"
