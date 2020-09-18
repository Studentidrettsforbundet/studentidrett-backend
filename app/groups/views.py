from django.shortcuts import render
from rest_framework import viewsets, permissions

from rest_framework.parsers import JSONParser

from .serializers import GroupSerializer
from .models import Group
from .permissions import GetGroupPermission

# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [GetGroupPermission]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


