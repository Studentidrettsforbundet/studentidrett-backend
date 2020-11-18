import factory

from cities.models import City


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = "Trondheim"
    region = "midt"


class CityFactoryT(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = "Trondheim"
    region = "midt"


class CityFactoryB(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = "Bergen"
    region = "vest"
