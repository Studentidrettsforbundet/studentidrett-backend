from django.urls import path
from .views import *

urlpatterns = [
    path('clubs/', club_list),
    path('clubs/<int:pk>/', club_detail),
]