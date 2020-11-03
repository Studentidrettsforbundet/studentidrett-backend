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
        city = self.request.query_params.get("city", None)
        sport = self.request.query_params.get("sport", None)
        club = self.request.query_params.get("club", None)

        if city is not None:
            query_param_invalid(city)
            try:
                city = int(city)
                city_queryset = Group.objects.filter(city__id=city)
            except ValueError:
                city_queryset = Group.objects.filter(city__name=city)
            queryset = queryset.intersection(city_queryset)

        if sport is not None:
            query_param_invalid(sport)
            try:
                sport = int(sport)
                sport_queryset = Group.objects.filter(sports__id=sport)
            except ValueError:
                sport_queryset = Group.objects.filter(sports__name=sport)
            queryset = queryset.intersection(sport_queryset)

        if club is not None:
            query_param_invalid(club)
            try:
                club = int(club)
                club_queryset = Group.objects.filter(club__id=club)
            except ValueError:
                club_queryset = Group.objects.filter(club__name=club)
            queryset = queryset.intersection(club_queryset)

        return queryset.order_by("name")
