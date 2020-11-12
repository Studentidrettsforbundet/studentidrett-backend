from rest_framework import viewsets

from app.utils import query_param_invalid
from clubs.permissions import GetClubPermission

from .models import Club
from .serializers import ClubSerializer


class ClubViewSet(viewsets.ModelViewSet):
    permission_classes = [GetClubPermission]
    queryset = Club.objects.all()
    serializer_class = ClubSerializer

    def get_queryset(self):
        queryset = self.queryset
        city = self.request.query_params.get("city", None)
        sport = self.request.query_params.get("sport", None)

        if city is not None:
            query_param_invalid(city)
            try:
                city = int(city)

                city_queryset = Club.objects.filter(city__id=city)
            except ValueError:
                city_queryset = Club.objects.filter(city__name=city)
            queryset = queryset.intersection(city_queryset)

        if sport is not None:
            query_param_invalid(sport)

            sport_queryset = Club.objects.none()
            for club in queryset:
                try:
                    sport = int(sport)
                    has_sport = club.groups.filter(sports__id=sport)
                    if has_sport:
                        club = Club.objects.filter(pk=club.pk)
                        sport_queryset = sport_queryset | club
                except ValueError:
                    has_sport = club.groups.filter(sports__name=sport)
                    if has_sport:
                        club = Club.objects.filter(pk=club.pk)
                        sport_queryset = sport_queryset | club
            queryset = queryset.intersection(sport_queryset)

        return queryset.order_by("name")
