from rest_framework import viewsets

from cities.models import City
from groups.models import Group

# from groups.permissions import GetGroupPermission
from groups.serializers import GroupSerializer
from sports.models import Sport

# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    # permission_classes = [GetGroupPermission]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        queryset = self.queryset
        city_name = self.request.query_params.get("city", None)
        sport_name = self.request.query_params.get("sport", None)

        if city_name is not None:
            try:
                city = City.objects.get(name=city_name)
                sport_queryset = queryset.filter(city=city.id)
            except City.DoesNotExist:
                city_queryset = Group.objects.none()

        if sport_name is not None:
            try:
                sport = Sport.objects.get(name=sport_name)
                sport_queryset = queryset.filter(sport=sport.id)
            except Sport.DoesNotExist:
                sport_queryset = Group.objects.none()

        if city_name and sport_name:
            return queryset.intersection(city_queryset, sport_queryset)
        elif city_name:
            return city_queryset
        elif sport_name:
            return sport_queryset
        else:
            return queryset
