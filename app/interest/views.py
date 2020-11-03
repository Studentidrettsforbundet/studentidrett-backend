from rest_framework import viewsets

from .models import Interest

# from .permissions import GetInterestPermission
from .serializers import InterestSerializer


class InterestViewSet(viewsets.ModelViewSet):
    # permission_classes = [GetInterestPermission]
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    http_method_names = ["get", "post", "head"]
