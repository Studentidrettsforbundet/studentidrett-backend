from rest_framework import viewsets

from .models import Club
from .serializers import ClubSerializer

# from clubs.permissions import GetClubPermission


class ClubViewSet(viewsets.ModelViewSet):
    # permission_classes = [GetClubPermission]
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

    def get_queryset(self):
        queryset = self.queryset
        city_name = self.request.query_params.get("city", None)
        if city_name is not None:
            queryset = Club.objects.filter(city__name=city_name)
        return queryset
