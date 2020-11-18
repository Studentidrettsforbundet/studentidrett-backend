import factory

from clubs.models import Club


class ClubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Club

    name = "GCIL"
    description = "The usual suspects"
    contact_email = factory.lazy_attribute(
        lambda club: f"contact@{club.name}.com".lower()
    )
    membership_fee = "100kr"
    register_info = "The standard procedure"


class BIClubFactory(ClubFactory):
    class Meta:
        model = Club

    name = "BI lions"
    description = "BI sports team"
    contact_email = "cheif@bilions.com"
    membership_fee = "money"
    register_info = "Please register"


class LongNameClubFactory(ClubFactory):
    class Meta:
        model = Club

    name = "N" * 256
