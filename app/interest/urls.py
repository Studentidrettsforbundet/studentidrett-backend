from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import InterestViewSet

router = DefaultRouter()
router.register(r"interest", InterestViewSet)

urlpatterns = [path("", include(router.urls))]
