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
from django.urls import include, path

from django.contrib import admin

import search.views as search_views

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls),
    path('', include('interest.urls')),
    path('', include('app.swagger_docs')),
    path('', include('groups.urls')),
    path('', include('sports.urls')),
    path('', include('cities.urls')),
    path('', include('clubs.urls')),
    path('', include('teams.urls')),
    #path('', include('search.urls'))
    path(r'search/', search_views.search, name='search')
=======
    path("admin/", admin.site.urls),
    path("", include("interest.urls")),
    path("", include("app.swagger_docs")),
    path("", include("groups.urls")),
    path("", include("sports.urls")),
    path("", include("cities.urls")),
    path("", include("clubs.urls")),
    path("", include("teams.urls")),
>>>>>>> eec2872d24657201c4242343aa9be0f1d4065fd6
]
