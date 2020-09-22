from rest_framework import viewsets

from groups.serializers import GroupSerializer
from groups.models import Group
from groups.permissions import GetGroupPermission

# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [GetGroupPermission]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


