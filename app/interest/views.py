from rest_framework import status, viewsets
from rest_framework.response import Response

from app.utils import is_allowed_origin

from .models import Interest

# from .permissions import GetInterestPermission
from .serializers import InterestSerializer


class InterestViewSet(viewsets.ModelViewSet):
    # permission_classes = [GetInterestPermission]
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    http_method_names = ["get", "post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        origin = request.headers["origin"]
        if not is_allowed_origin(origin + "/"):
            return Response(
                f"{origin} is not allowed to post interests.",
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
