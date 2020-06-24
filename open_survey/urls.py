from django.contrib import admin
from django.urls import path, include
from main.views import HomeView, consent, autologin, logout_user, take_survey, FaqView, VisionView, \
    CitizenScienceView, DataView, TeamView, set_language_custom, delete_all_openhuman_files

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("autologin/<int:oh_id>/", autologin, name="autologin"),
    path("consent/", consent, name="consent"),
    path("logout/", logout_user, name="logout"),
    path("survey/", take_survey, name="take_survey"),
    path("team/", TeamView.as_view(), name="team"),
    path("faq/", FaqView.as_view(), name="faq"),
    path("vision/", VisionView.as_view(), name="vision"),
    path("citizen-science/", CitizenScienceView.as_view(), name="citizen_science"),
    path("data/", DataView.as_view(), name="data"),

    path("delete-all-openhuman-files/", delete_all_openhuman_files, name="delete_all_openhuman_files"),

    path("i18n/", set_language_custom, name="set_language_custom"),
]

urlpatterns += [path("openhumans/", include("openhumans.urls"))]
