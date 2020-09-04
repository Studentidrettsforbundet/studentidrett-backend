from cities.views import city_list
from django.urls import path

urlpatterns = [
    path('cities/', city_list)
]