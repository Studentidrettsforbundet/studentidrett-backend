from clubs.views import ClubViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'clubs',ClubViewSet)

urlpatterns = [
    path('', include(router.urls))
]