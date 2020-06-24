from django.views.i18n import set_language
from django.views.generic import TemplateView
from django.views.generic.base import View
from openhumans.models import OpenHumansMember
from .models import ReportToken
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
import datetime
from .helpers import create_openclinica_event, get_openclinica_token, send_user_survey_link

import logging
logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = "main/home.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                self.files = self.request.user.openhumansmember.list_files()
            except Exception:
                logout(request)
                return redirect("/")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        if self.request.user.is_authenticated:
            openhumansmember = self.request.user.openhumansmember

            context.update(
                {
                    "openhumansmember": openhumansmember,
                    "files": self.files
                }
            )

        # Not logged in.
        else:
            context.update({"openhumans_login_url": OpenHumansMember.get_auth_url()})

        return context


class ConsentView(View):
    def get(self, request, *args, **kwargs):
        logged_in = False
        if request.user.is_authenticated:
            logged_in = True
            survey_member = request.user.openhumansmember.surveyaccount
        token_string = request.GET.get("login_token", None)
        oh_id = request.GET.get("oh_id", None)
        if token_string and oh_id:
            token = ReportToken.objects.get(token=token_string)
            if token.is_valid():
                logged_in = True
                oh_member = OpenHumansMember.objects.get(oh_id=oh_id)
                survey_member = oh_member.surveyaccount
        if logged_in:
            if request.GET.get("consent"):
                if request.GET["consent"] == "1":
                   survey_member.consent_given = True
                   survey_member.save()
                   if token_string and oh_id:
                       return redirect(
                           "{}?login_token={}".format(reverse("take_survey", kwargs={"oh_id": oh_id}), token_string))
                   elif request.user.is_authenticated:
                       get_openclinica_token(survey_member)
                       send_user_survey_link(survey_member)
                       messages.add_message(request, messages.INFO, _("Your consent has been saved. You should now get "
                                                                      "an email to get started with your survey!"))
                elif request.GET["consent"] == "0":
                    survey_member.consent_given = False
                    survey_member.save()
                    if request.user.is_authenticated:
                        messages.add_message(request, messages.INFO, _("Your consent has been withdrawn, you will not "
                                                                       "receive any more daily emails."))
                    else:
                        return redirect("{}?consent_withdrawn=1".format(reverse("home")))

        return redirect("home")


def take_survey(request, oh_id):
    logged_in = False
    if request.user.is_authenticated:
        if request.user.openhumansmember.oh_id == oh_id:
            logged_in = True
            oh_member = request.user.openhumansmember
            survey_member = oh_member.surveyaccount
    token_string = request.GET.get("login_token", None)
    if token_string:
        token = ReportToken.objects.get(token=token_string)
        if token.is_valid():
            logged_in = True
            oh_member = OpenHumansMember.objects.get(oh_id=oh_id)
            survey_member = oh_member.surveyaccount
    if logged_in:
        if survey_member.consent_given:
            if survey_member.last_survey != datetime.date.today():
                create_openclinica_event(survey_member, "SE_DAILY", str(datetime.date.today()))
                survey_member.last_survey = datetime.date.today()
                survey_member.save()
            return redirect(settings.OPENCLINICA_PARTICIPATE_LINK + "?accessCode={}".format(survey_member.survey_token))
        else:
            return redirect("{}?oh_id={}&login_token={}".format(reverse("home"), oh_id,  token_string))
    else:
        return redirect('home')


def logout_user(request):
    """
    Logout user.
    """
    if request.method == "POST":
        logout(request)
    redirect_url = settings.LOGOUT_REDIRECT_URL
    if not redirect_url:
        redirect_url = "home"
    return redirect(redirect_url)


class FaqView(TemplateView):
    template_name = "main/faq.html"


class TeamView(TemplateView):
    template_name = "main/faq.html"


class VisionView(TemplateView):
    template_name = "main/vision.html"


class CitizenScienceView(TemplateView):
    template_name = "main/citizen-science.html"


class DataView(TemplateView):
    template_name = "main/data.html"


def set_language_custom(request):
    if request.user.is_authenticated and request.POST.get('language'):
        if request.POST['language'] in [lang[0] for lang in settings.LANGUAGES]:
            request.user.openhumansmember.surveyaccount.language = request.POST['language']
            request.user.openhumansmember.surveyaccount.save()

    return set_language(request)
