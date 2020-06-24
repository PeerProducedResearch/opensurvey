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
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.http import HttpResponseForbidden
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


def autologin(request, oh_id):
    if not request.user.is_authenticated:
        token_string = request.GET.get("login_token", None)
        if token_string:
            token = ReportToken.objects.get(token=token_string)
            if token.is_valid():
                try:
                    oh_member = OpenHumansMember.objects.get(oh_id=oh_id)
                    auth_login(request, oh_member.user)
                except:
                    pass
    if request.user.is_authenticated:
        if request.GET.get('next'):
            return redirect(request.GET['next'])
        else:
            return redirect('home')
    else:
        return HttpResponseForbidden()


@login_required()
@require_POST
def consent(request):
    survey_member = request.user.openhumansmember.surveyaccount
    if survey_member.consent_given == False:
       survey_member.consent_given = True
       survey_member.save()
       if survey_member.last_survey == datetime.date.today():
           messages.add_message(request, messages.INFO, _("Your consent has been saved. You should already "
                                                          "have gotten an email earlier today to get started "
                                                          "with your survey!"))
       else:
           get_openclinica_token(survey_member)
           send_user_survey_link(survey_member)
           messages.add_message(request, messages.INFO, _("Your consent has been saved. You should now get "
                                                          "an email to get started with your survey!"))
    else:
        survey_member.consent_given = False
        survey_member.save()
        messages.add_message(request, messages.INFO, _("Your consent has been withdrawn, you will not "
                                                       "receive any more daily emails."))
    return redirect("home")


@login_required()
def take_survey(request):
    oh_member = request.user.openhumansmember
    survey_member = oh_member.surveyaccount
    if survey_member.consent_given:
        if survey_member.last_survey != datetime.date.today():
            create_openclinica_event(survey_member, "SE_DAILY", str(datetime.date.today()))
            survey_member.last_survey = datetime.date.today()
            survey_member.save()
        return redirect(settings.OPENCLINICA_PARTICIPATE_LINK + "?accessCode={}".format(survey_member.survey_token))
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
            context.update(
                {
                    "files": self.files
                }
            )

        return context


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


@login_required
def delete_all_openhuman_files(request):
    oh_member = request.user.openhumansmember
    oh_member.delete_all_files()

    return redirect('faq')
