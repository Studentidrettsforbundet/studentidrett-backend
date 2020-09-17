from .models import Club
from cities.models import City
from .serializers import ClubSerializer
from rest_framework import viewsets
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Create your views here.

# Automatically provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

    def get_queryset(self):
        queryset = self.queryset
        city_name = self.request.query_params.get('city', None)
        if city_name is not None:
            city = City.objects.filter(name=city_name)
            if city.count() == 0:
                queryset = Club.objects.none()
            elif city.count() == 1:
                queryset = queryset.filter(city=city[0].id)
            else:
                result = {}
                for num in city:
                    result += queryset.filter(city=num)
                queryset = result
        return queryset




