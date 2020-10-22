from rest_framework import permissions, viewsets

from sports.models import Sport
from sports.serializers import SportSerializer

from groups.views import GroupViewSet
from groups.models import Group
from cities.models import City

# Create your views here.


class SportViewSet(viewsets.ModelViewSet):
    serializer_class = SportSerializer
    queryset = Sport.objects.all()
    #permission_classes = [permissions.AllowAny]


    def get_queryset(self):
        queryset = self.queryset

        city_name = self.request.query_params.get("city", None)

        if city_name is not None:
            groups_in_city = Group.objects.filter(city__name=city_name)

            if groups_in_city.exists():
                for group in groups_in_city:
                    sport_queryset = group.sports.all()

                    print("SPORTENE:", sport_queryset)
                    queryset = queryset.intersection(sport_queryset)
            else:
                queryset = Sport.objects.none()

        return queryset.order_by("name")