from django.urls import path, include
from rest_framework.routers import DefaultRouter

from groups.views import GroupViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls))
]
