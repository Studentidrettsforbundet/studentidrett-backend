import factory
from clubs.models import Club
from cities.models import City
from cities.factories.city_factories import CityFactory, CityFactoryT


class ClubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Club

    name = "GCIL"
    description = "The usual suspects"
    contact_email = factory.lazy_attribute(lambda club: f"contact@{club.name}.com".lower())
    membership_fee = "100kr"
    register_info = "The standard procedure"
    # city = factory.SubFactory(CityFactoryT)


class BIClubFactory(ClubFactory):
    class Meta:
        model = Club

    name = "BI lions"
    # city = factory.SubFactory(CityFactory(name="Oslo", region="ØST"))
    description = "BI sports team"
    contact_email = "cheif@bilions.com"
    membership_fee = "about all of your yearly income"
    register_info = "You'll have to buy champagne for the entire club"


class LongNameClubFactory(ClubFactory):
    class Meta:
        model = Club

    name = "N"*256
    # city = factory.SubFactory(CityFactoryT)

# TODO: Fix the issue with city foreign key
