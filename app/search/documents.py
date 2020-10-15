from django_elasticsearch_dsl import Document, Index, fields

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
    city = fields.ObjectField(properties={"id": fields.IntegerField()})

    class Django:
        model = Club

        # Index on name, but including the other fields to include them in the resultbase
        fields = [
            "id",
            "name",
            "description",
            "contact_email",
            "pricing",
            "register_info",
        ]


@CITY_INDEX.doc_type
class CityDocument(Document):
    class Django:
        model = City

        fields = ["id", "name", "region"]


@GROUP_INDEX.doc_type
class GroupDocument(Document):
    city = fields.ObjectField(properties={"id": fields.IntegerField()})
    club = fields.ObjectField(properties={"id": fields.IntegerField()})
    sports = fields.NestedField(properties={"id": fields.IntegerField()})

    class Django:
        model = Group

        fields = ["id", "name", "description", "cover_photo", "contact_email"]


@SPORT_INDEX.doc_type
class SportDocument(Document):
    class Django:
        model = Sport

        fields = ["id", "name"]
