from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('clubs/', club_list),
    path('clubs/<int:pk>/', club_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
