from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clubSports.views import ClubSportViewSet

router = DefaultRouter()
router.register(r'clubSports', ClubSportViewSet)

urlpatterns = [
    path('', include(router.urls))
]
