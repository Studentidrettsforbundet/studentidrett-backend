from django.urls import path, include
from rest_framework.routers import DefaultRouter

from sports.views import SportViewSet

router = DefaultRouter()
router.register(r'sports', SportViewSet)

urlpatterns = [
    path('', include(router.urls))
]
