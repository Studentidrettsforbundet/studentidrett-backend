from django.urls import path, include
from .views import ClubViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'clubs', ClubViewSet)


urlpatterns = [
    path('', include(router.urls)),
]