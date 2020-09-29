from django_elasticsearch_dsl import Document, Index, fields
from clubs.models import Club

CLUB_INDEX = Index('clubs')

@CLUB_INDEX.doc_type
class ClubDocument(Document):
    class Django:
        #name = fields.TextField(attr='name')

        model = Club

        # Index on city, but including the other fields to include them in the resultbasepy
        fields = [
            'name',
            'description',
            'contact_email',
            'pricing',
            'register_info'
        ]