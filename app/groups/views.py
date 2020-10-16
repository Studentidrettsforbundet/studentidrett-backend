from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from groups.models import Group

# from groups.permissions import GetGroupPermission
from groups.serializers import GroupSerializer

# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    # permission_classes = [GetGroupPermission]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend]
