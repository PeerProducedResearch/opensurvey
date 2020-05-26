from django.conf import settings
import requests
import json
from .models import ReportToken
from urllib.parse import urljoin
from django.shortcuts import reverse


def get_access_token():
    url = 'https://opencovid.build.openclinica.io/user-service/api/oauth/token'
    headers = {'Content-Type': "application/json"}
    data = json.dumps(
        {'username': settings.OPENCLINICA_USERNAME, 'password': settings.OPENCLINICA_PASSWORD}
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


def create_token_url(member, token):
    url = urljoin(
        settings.OPENHUMANS_APP_BASE_URL,
        'survey') + "/" + member.oh_id + "?login_token={}".format(token.token)
    return url


def send_user_survey_link(survey_member):
    token = ReportToken(member=survey_member.member)
    token.save()
    url = create_token_url(survey_member.member, token)
    survey_member.member.message(
        subject="Here's your survey link!",
        message="Please use this URL to fill out the survey: {}".format(url))
