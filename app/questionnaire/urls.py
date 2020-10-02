from django.urls import include, path

from rest_framework.routers import DefaultRouter

from questionnaire.views import QuestionnaireViewSet

router = DefaultRouter()
router.register(r"questionnaire", QuestionnaireViewSet)

urlpatterns = [path("", include(router.urls))]
