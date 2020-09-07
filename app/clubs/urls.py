from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clubs.views import ClubViewSet

router = DefaultRouter()
router.register(r'clubs', ClubViewSet)

urlpatterns = [
    path('', include(router.urls))
]
