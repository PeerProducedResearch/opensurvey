"""open_survey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.urls import path, include
from main.views import HomeView, ConsentView, logout_user, take_survey, FaqView, VisionView, \
    CitizenScienceView, DataView, TeamView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("consent/", ConsentView.as_view(), name="consent"),
    path("logout/", logout_user, name="logout"),
    path("survey/<int:oh_id>/", take_survey, name="take_survey"),
    path("team/", TeamView.as_view(), name="team"),
    path("faq/", FaqView.as_view(), name="faq"),
    path("vision/", VisionView.as_view(), name="vision"),
    path("citizen-science/", CitizenScienceView.as_view(), name="citizen_science"),
    path("data/", DataView.as_view(), name="data"),

    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += [path("openhumans/", include("openhumans.urls"))]
