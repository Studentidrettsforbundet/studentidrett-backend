from cities.views import city_list, city_detail
from django.urls import path

urlpatterns = [
    path('cities/', city_list, name="city_list"),
    path('cities/<int:pk>', city_detail, name="city_detail")
]