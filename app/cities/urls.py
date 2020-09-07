from cities.views import CityViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cities',CityViewSet)

urlpatterns = [
    path('', include(router.urls))
]