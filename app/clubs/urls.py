from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from django.conf.urls import include

urlpatterns = [
    path('clubs/', ClubList.as_view()),
    path('clubs/<int:pk>/', ClubDetail.as_view()),
    path('users/', UserList.as_view()),
    path('users/<int:pk>', UserDetail.as_view()),
    path('api-auth/', include('rest_framework.urls'))
]

urlpatterns = format_suffix_patterns(urlpatterns)

