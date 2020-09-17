from django.shortcuts import render
from rest_framework import viewsets, permissions

from rest_framework.parsers import JSONParser

from groups.serializers import GroupSerializer
from groups.models import Group

# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


