from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import StringField

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

        fields = [
            "id",
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
    labels = fields.NestedField(properties={"text": StringField()})

    class Django:
        model = Sport
        fields = ["id", "name"]
