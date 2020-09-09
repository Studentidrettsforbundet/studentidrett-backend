from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework import renderers
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'clubs', ClubViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]