from django.shortcuts import render
from rest_framework import viewsets, permissions

from rest_framework.parsers import JSONParser

from sports.serializers import SportSerializer
from sports.models import Sport

# Create your views here.


class SportViewSet(viewsets.ModelViewSet):
    serializer_class = SportSerializer
    queryset = Sport.objects.all()
    permission_classes = [permissions.AllowAny]
