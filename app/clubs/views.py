from rest_framework import viewsets

from app.utils import query_param_invalid

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
        sport_name = self.request.query_params.get("sport", None)

        if city_name is not None:
            query_param_invalid(city_name)

            city_queryset = Club.objects.filter(city__name=city_name)
            queryset = queryset.intersection(city_queryset)

        if sport_name is not None:
            query_param_invalid(sport_name)
            sport_queryset = Club.objects.none()
            for club in queryset:
                has_sport = club.groups.filter(sports__name=sport_name)
                if has_sport:
                    club = Club.objects.filter(pk=club.pk)
                    sport_queryset = sport_queryset | club
            queryset = queryset.intersection(sport_queryset)

        return queryset.order_by("name")
