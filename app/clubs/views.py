from cities.models import City
from clubs.permissions import GetClubPermission
from rest_framework import viewsets

from .models import Club
from .serializers import ClubSerializer


class ClubViewSet(viewsets.ModelViewSet):
    permission_classes = [GetClubPermission]
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

    def get_queryset(self):
        queryset = self.queryset
        city_name = self.request.query_params.get("city", None)
        if city_name is not None:
            city = City.objects.filter(name=city_name)
            if not city.count():
                queryset = Club.objects.none()
            elif city.count() == 1:
                queryset = queryset.filter(city=city[0].id)
            else:
                result = {}
                for num in city:
                    result += queryset.filter(city=num)
                queryset = result
        return queryset
