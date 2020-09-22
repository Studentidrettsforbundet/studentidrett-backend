from .permissions import GetInterestPermission
from rest_framework import viewsets

from .models import Interest
from .serializers import InterestSerializer

# Create your views here.


class InterestViewSet(viewsets.ModelViewSet):
    permission_classes = [GetInterestPermission]
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    http_method_names = ['get', 'post', 'head']
