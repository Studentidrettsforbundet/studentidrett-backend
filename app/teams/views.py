from rest_framework import viewsets

from app.utils import query_param_invalid

from .models import Team
from .serializers import TeamSerializer

# from teams.permissions import GetPermission


# Create your views here.


class TeamViewSet(viewsets.ModelViewSet):
    # permission_classes = [GetPermission]
    queryset = Team.objects.all().order_by("id")
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = self.queryset
        group = self.request.query_params.get("group", None)

        if group is not None:
            query_param_invalid(group)
            try:
                group = int(group)
                group_queryset = Team.objects.filter(group__id=group)
            except ValueError:
                group_queryset = Team.objects.filter(group__name=group)
            queryset = queryset.intersection(group_queryset)

        return queryset.order_by("id")
