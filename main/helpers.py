import datetime
import requests
import json
from urllib.parse import urljoin
from .models import ReportToken
from django.utils import translation
from django.conf import settings
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _


def get_access_token(download=False):
    url = 'https://opencovid.build.openclinica.io/user-service/api/oauth/token'
    headers = {'Content-Type': "application/json"}
    data = json.dumps(
        {'username': settings.OPENCLINICA_SITE_USERNAME, 'password': settings.OPENCLINICA_SITE_PASSWORD}
    )
    if download:
        data = json.dumps(
            {'username': settings.OPENCLINICA_DATA_USERNAME, 'password': settings.OPENCLINICA_DATA_PASSWORD}
        )
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError("{} returned: {}".format(url, response.text))


def create_openclinica_user(survey_member):
    headers = {
        "Authorization": "bearer {}".format(get_access_token()),
        "Content-Type": "application/json"
    }
    data = {
        "identifier": survey_member.member.oh_id,
        "subjectKey": survey_member.member.oh_id
        }
    url = "https://opencovid.openclinica.io/OpenClinica/pages/auth/api/clinicaldata/studies/{}/sites/{}/participants?register=y".format(
        settings.OPENCLINICA_STUDY, settings.OPENCLINICA_SITE
    )
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError("{} returned: {}".format(url, response.text))


def create_openclinica_event(survey_member, event, date):
    headers = {
        "Authorization": "bearer {}".format(get_access_token()),
        "Content-Type": "application/json"
    }
    data = {
        "endDate": date,
        "startDate": date,
        "studyEventOID": event,
        "subjectKey": survey_member.member.oh_id,
        }

    url = "https://opencovid.openclinica.io/OpenClinica/pages/auth/api/clinicaldata/studies/{}/sites/{}/events".format(
        settings.OPENCLINICA_STUDY, settings.OPENCLINICA_SITE
    )
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.text
    else:
        try:
            # Does onboarding event already exists on OpenClinica ?
            if response.json().get("message") == "errorCode.eventAlreadyExists":
                return response.text
        except:
            raise ValueError("{} returned: {}".format(url, response.text))


def get_openclinica_token(survey_member):
    headers = {
        "Authorization": "bearer {}".format(get_access_token()),
        "Content-Type": "application/json"
    }
    url = "https://opencovid.openclinica.io/OpenClinica/pages/auth/api/clinicaldata/studies/{}/sites/{}/participant?includeParticipateInfo=y&participantID={}".format(
        settings.OPENCLINICA_STUDY, settings.OPENCLINICA_SITE, survey_member.member.oh_id
    )
    response = requests.get(url, headers=headers)
    print(response.json())
    if response.status_code == 200:
        survey_member.survey_token = response.json()['accessCode']
        survey_member.save()
        return response.text
    else:
        raise ValueError("{} returned: {}".format(url, response.text))


def create_autologin_url(member, token):
    url = urljoin(
        settings.OPENHUMANS_APP_BASE_URL,
        reverse("autologin", kwargs={"oh_id":member.oh_id}) + "?login_token={}".format(token.token)
    )
    return url


def create_survey_url(member, token):
    url = create_autologin_url(member, token) + "&next=/survey"
    return url


def send_user_survey_link(survey_member):
    token = ReportToken(member=survey_member.member)
    token.save()
    url = create_survey_url(survey_member.member, token)
    withdraw_url = create_autologin_url(survey_member.member, token)
    saved_language = survey_member.member.surveyaccount.language
    translation.activate(saved_language)
    survey_member.member.message(
        subject=_("Here's your survey link!"),
        message="{}: {}\n\n\n{}: {}".format(
            _("Please use this link to fill out the survey"),
            url,
            _("If you don't want to take part in the survey anymore, please use this link and click on \"WITHDRAW MY CONSENT\""),
            withdraw_url
        )
    )
    survey_member.last_email = datetime.date.today()
    survey_member.save()
