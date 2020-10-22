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
        group_name = self.request.query_params.get("group", None)

        if group_name is not None:
            query_param_invalid(group_name)
            group_queryset = Team.objects.filter(group__name=group_name)
            queryset = queryset.intersection(group_queryset)

        return queryset.order_by("id")
