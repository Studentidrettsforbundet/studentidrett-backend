from rest_framework import permissions
from rest_framework import viewsets

from cities.models import City
from cities.serializers import CitySerializer


# Create your views here.


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = City.objects.all()
    serializer_class = CitySerializer
