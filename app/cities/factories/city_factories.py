import factory
from cities.models import City


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = "Trondheim"