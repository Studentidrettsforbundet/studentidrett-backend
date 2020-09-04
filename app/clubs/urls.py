from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('clubs/', ClubList.as_view()),
    path('clubs/<int:pk>/', ClubDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
