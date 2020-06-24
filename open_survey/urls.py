from django.contrib import admin
from django.urls import path, include
from main.views import HomeView, ConsentView, logout_user, take_survey, FaqView, VisionView, \
    CitizenScienceView, DataView, TeamView, set_language_custom

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

    path("i18n/", set_language_custom, name="set_language_custom"),
]

urlpatterns += [path("openhumans/", include("openhumans.urls"))]
