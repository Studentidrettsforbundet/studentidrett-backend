from django.urls import include, path

from rest_framework.routers import DefaultRouter

from questionnaire.views import QuestionnaireViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r"questionnaire", QuestionnaireViewSet)
router.register(r"questions", QuestionViewSet)

urlpatterns = [path("", include(router.urls))]
