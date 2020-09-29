from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import ParseError

from app.enums import Region
from cities.models import City
from cities.serializers import CitySerializer

# Create your views here.


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        queryset = self.queryset
        region = self.request.query_params.get("region", None)
        if region is not None:
            if region not in Region.values:
                raise ParseError(
                    detail="Invalid region name. Only permitted names are: [nord, midt, vest, sør, øst]",
                    code=status.HTTP_400_BAD_REQUEST,
                )
            else:
                queryset = queryset.filter(region=region)
        return queryset
