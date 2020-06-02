from django.shortcuts import render
from django.views.generic import TemplateView
from openhumans.models import OpenHumansMember
from .models import ReportToken
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
import datetime
from .helpers import create_openclinica_event

# Create your views here.


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


def logout_user(request):
    """
    Logout user.
    """
    if request.method == "POST":
        logout(request)
    redirect_url = settings.LOGOUT_REDIRECT_URL
    if not redirect_url:
        redirect_url = "/"
    return redirect(redirect_url)


def take_survey(request, oh_id):
    logged_in = False
    if request.user.is_authenticated:
        if request.user.openhumansmember.oh_id == oh_id:
            print('user is logged in')
            logged_in = True
    token_string = request.GET.get('login_token', None)
    if token_string:
        token = ReportToken.objects.get(token=token_string)
        if token.is_valid():
            print('token is valid')
            logged_in = True
    if logged_in:
        oh_member = OpenHumansMember.objects.get(oh_id=oh_id)
        survey_member = oh_member.surveyaccount
        if survey_member.last_survey != datetime.date.today():
            create_openclinica_event(survey_member, "SE_DAILY", str(datetime.date.today()))
            survey_member.last_survey = datetime.date.today()
            survey_member.save()
        return redirect(settings.OPENCLINICA_PARTICIPATE_LINK + "?accessCode={}".format(survey_member.survey_token))
    else:
        redirect('/')


def faq(request):
    """
    Logout user.
    """
    return render(request, 'main/faq.html')


def team(request):
    """
    Logout user.
    """
    return render(request, 'main/team.html')


def vision(request):
    """
    Logout user.
    """
    return render(request, 'main/vision.html')
