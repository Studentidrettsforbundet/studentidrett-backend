from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Interest
from .permissions import GetInterestPermission
from .serializers import InterestSerializer


class InterestViewSet(viewsets.ModelViewSet):
    permission_classes = [GetInterestPermission]
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    http_method_names = ["get", "post", "head"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not request.COOKIES.get("csrftoken"):
            return Response(
                'No "csrftoken" found in cookies', status=status.HTTP_400_BAD_REQUEST
            )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(cookie_key=self.request.COOKIES.get("csrftoken"))
