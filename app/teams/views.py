from rest_framework import viewsets

from .models import Team
from .serializers import TeamSerializer

# from teams.permissions import GetPermission


# Create your views here.


class TeamViewSet(viewsets.ModelViewSet):
    # permission_classes = [GetPermission]
    queryset = Team.objects.all().order_by("id")
    serializer_class = TeamSerializer
