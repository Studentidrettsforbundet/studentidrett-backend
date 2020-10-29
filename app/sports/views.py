from rest_framework import permissions, viewsets

from groups.models import Group
from sports.models import Sport
from sports.serializers import SportSerializer

# Create your views here.


class SportViewSet(viewsets.ModelViewSet):
    serializer_class = SportSerializer
    queryset = Sport.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = self.queryset

        city = self.request.query_params.get("city", None)

        if city is not None:
            queryset = Sport.objects.none()
            try:
                city = int(city)
                groups_in_city = Group.objects.filter(city__id=city)
            except ValueError:
                groups_in_city = Group.objects.filter(city__name=city)

            if groups_in_city.exists():
                for group in groups_in_city:
                    sport_queryset = group.sports.all()
                    queryset = queryset.union(sport_queryset)

        return queryset
