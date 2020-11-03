"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import include, path, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

import search.views as search_views
from app import settings

from django.contrib import admin

openapi_info = openapi.Info(
    title="NSI API",
    default_version="v2",
    description="API to access NSI",
    license=openapi.License(name="Apache v2 License"),
)

schema_view = get_schema_view(
    openapi_info,
    public=True,
)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("interest.urls")),
        path("", include("groups.urls")),
        path("", include("sports.urls")),
        path("", include("cities.urls")),
        path("", include("clubs.urls")),
        path("", include("teams.urls")),
        path(r"search/", search_views.global_search, name="global_search"),
        path("", include("questionnaire.urls")),
        re_path(
            r"^doc(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "doc/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
