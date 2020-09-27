from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cities.views import CityViewSet

router = DefaultRouter()
router.register(r'cities', CityViewSet)

urlpatterns = [
    path('', include(router.urls))
]
