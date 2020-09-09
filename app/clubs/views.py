from django.views.decorators.csrf import csrf_exempt

from .models import Club
from .serializers import ClubSerializer, UserSerializer
from rest_framework import generics, renderers
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets

# Create your views here.

@api_view (['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list',request = request, format=format),
        'clubs': reverse('club-list', request=request, format=format)
    })

#Automatically provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions
class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


#Automatically  provides the 'list' and 'detail' actions
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer




