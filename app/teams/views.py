from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TeamSerializer
from .models import Team
from teams.permissions import GetPermission

# Create your views here.


class TeamViewSet(viewsets.ModelViewSet):
    permission_classes = [GetPermission]
    queryset = Team.objects.all().order_by('id')
    serializer_class = TeamSerializer

