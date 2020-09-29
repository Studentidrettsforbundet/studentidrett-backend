from rest_framework import permissions, viewsets

from sports.models import Sport
from sports.serializers import SportSerializer

# Create your views here.


class SportViewSet(viewsets.ModelViewSet):
    serializer_class = SportSerializer
    queryset = Sport.objects.all()
    permission_classes = [permissions.AllowAny]
