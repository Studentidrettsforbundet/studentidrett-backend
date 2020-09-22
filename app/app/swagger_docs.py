from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import re_path, path

schema_view = get_schema_view(
    openapi.Info(
        title="NSI API",
        default_version='v1',
        description="NSI",
        contact=openapi.Contact(email="oddandreowren@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns=[
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc')
]