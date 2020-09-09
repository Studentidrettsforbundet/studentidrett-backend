from .models import Club
from .serializers import ClubSerializer
from rest_framework import viewsets

# Create your views here.

# Automatically provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


