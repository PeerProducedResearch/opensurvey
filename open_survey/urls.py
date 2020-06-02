"""open_survey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from main.views import HomeView, logout_user, take_survey, team, faq, vision

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("logout/", logout_user, name="logout"),
    path('survey/<int:oh_id>/', take_survey, name='take_survey'),
    path('team/', team, name='team'),
    path('faq/', faq, name='faq'),
    path('vision/', vision, name='vision'),
]

urlpatterns += [path("openhumans/", include("openhumans.urls"))]
