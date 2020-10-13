from django_elasticsearch_dsl import Document, Index

from cities.models import City
from clubs.models import Club
from groups.models import Group
from sports.models import Sport

CLUB_INDEX = Index("clubs")
CITY_INDEX = Index("cities")
GROUP_INDEX = Index("groups")
SPORT_INDEX = Index("sports")


@CLUB_INDEX.doc_type
class ClubDocument(Document):
    class Django:
        model = Club

        # Index on name, but including the other fields to include them in the resultbase
        fields = [
            "name",
            "description",
            "contact_email",
            "membership_fee",
            "register_info",
        ]


@CITY_INDEX.doc_type
class CityDocument(Document):
    class Django:
        model = City

        fields = ["name", "region"]


@GROUP_INDEX.doc_type
class GroupDocument(Document):
    class Django:
        model = Group

        fields = ["name", "description", "cover_photo", "contact_email"]


@SPORT_INDEX.doc_type
class SportDocument(Document):
    class Django:
        model = Sport

        fields = ["name"]
