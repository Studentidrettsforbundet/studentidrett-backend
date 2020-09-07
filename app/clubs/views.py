from rest_framework import viewsets
from rest_framework import permissions

from clubs.models import Club
from clubs.serializers import ClubSerializer

# Create your views here.


class ClubViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (permissions.AllowAny,)
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
