from django.shortcuts import render
from rest_framework import viewsets, permissions

from rest_framework.parsers import JSONParser

from clubSports.serializers import ClubSportSerializer
from clubSports.models import ClubSport

# Create your views here.


class ClubSportViewSet(viewsets.ModelViewSet):
    queryset = ClubSport.objects.all()
    serializer_class = ClubSportSerializer


