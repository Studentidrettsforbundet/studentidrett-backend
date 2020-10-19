from rest_framework import permissions, viewsets

from sports.models import Sport
from sports.serializers import SportSerializer

from groups.views import GroupViewSet
from cities.model import City

# Create your views here.


class SportViewSet(viewsets.ModelViewSet):
    serializer_class = SportSerializer
    queryset = Sport.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = self.queryset

        # Get all groups that include this sport
        groups_with_sport = Sport.group_set.all()
        cities = City.objects.none()

        if groups_with_sport.exists():
            for group in groups_with_sport:
                cities.append(group.get_queryset)
            if not cities.count():
                queryset = Sport.objects.none()
            elif cities.count() == 1:
                queryset = queryset.filter(city=cities[0].id)
            else:
                result = {}
                for num in cities:
                    result += queryset.filter(city=num)
                queryset = result

        return queryset