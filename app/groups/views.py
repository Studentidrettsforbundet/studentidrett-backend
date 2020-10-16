from rest_framework import viewsets

from cities.models import City
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

        if city_name or sport_name:

            if city_name is not None:
                city = City.objects.filter(name=city_name)
                if not city.count():
                    queryset = Group.objects.none()
                elif city.count() == 1:
                    queryset = queryset.filter(city=city[0].id)
                else:
                    result = {}
                    for num in city:
                        result += queryset.filter(city=num)
                    queryset = result
        return queryset
