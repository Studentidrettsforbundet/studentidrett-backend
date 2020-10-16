import factory
from clubs.models import Club


class ClubFactory(factory.Factory):
    class Meta:
        model = Club

    name = "GCIL"
    description = "The usual suspects"
    contact_email = "contact@gcil.com"
    membership_fee = "free"
    register_info = "The usual hazing procedure"