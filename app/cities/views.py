from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from app.enums import Region
from cities.models import City
from cities.serializers import CitySerializer

# Create your views here.


class CityViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def list(self, request, *args, **kwargs):
        queryset = CitySerializer(self.get_queryset(), many=True)
        region_dict = dict({"nord": [], "midt": [], "vest": [], "sor": [], "ost": []})
        for key in region_dict.keys():
            region_dict[key] = list(filter(lambda i: i["region"] == key, queryset.data))
        headers = self.get_success_headers(request)
        return Response(region_dict, status=status.HTTP_200_OK, headers=headers)

    def get_queryset(self):
        queryset = self.queryset
        region = self.request.query_params.get("region", None)
        if region is not None:
            if region not in Region.values:
                raise NotFound(
                    detail="Invalid region name. Only permitted names are: ["
                    + ", ".join(Region.values)
                    + "]",
                    code=status.HTTP_404_NOT_FOUND,
                )
            else:
                queryset = queryset.filter(region=region)
        return queryset
