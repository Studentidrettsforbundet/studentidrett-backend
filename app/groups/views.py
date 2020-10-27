from rest_framework import viewsets

from app.utils import query_param_invalid
from groups.models import Group

# from groups.permissions import GetGroupPermission
from groups.serializers import GroupSerializer

# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    # permission_classes = [GetGroupPermission]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        queryset = self.queryset
        city_name = self.request.query_params.get("city", None)
        sport_name = self.request.query_params.get("sport", None)
        club_name = self.request.query_params.get("club", None)

        if city_name is not None:
            query_param_invalid(city_name)
            city_queryset = Group.objects.filter(city__name=city_name)
            queryset = queryset.intersection(city_queryset)

        if sport_name is not None:
            query_param_invalid(sport_name)
            sport_queryset = Group.objects.filter(sports__name=sport_name)
            queryset = queryset.intersection(sport_queryset)

        if club_name is not None:
            query_param_invalid(club_name)
            club_queryset = Group.objects.filter(club__name=club_name)
            queryset = queryset.intersection(club_queryset)

        return queryset.order_by("name")
