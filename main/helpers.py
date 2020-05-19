from django.conf import settings
import requests
import json


def get_access_token():
    url = 'https://opencovid.build.openclinica.io/user-service/api/oauth/token'
    headers = {'Content-Type': "application/json"}
    data = json.dumps(
        {'username': settings.OPENCLINICA_USERNAME, 'password': settings.OPENCLINICA_PASSWORD}
    )
    response = requests.post(url, headers=headers, data=data)
    return response.text


def create_openclinica_user(survey_member):

    requests

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
    print(response.text)


def create_openclinica_event(survey_member, event, date):
    headers = {
        "Authorization": "bearer {}".format(get_access_token()),
        "Content-Type": "application/json"
    }
    data = {
        "endDate": date,
        "startDate": date,
        "studyEventOID": event,
        "subjectKey": survey_member.member.oh_id
        }

    url = "https://opencovid.openclinica.io/OpenClinica/pages/auth/api/clinicaldata/studies/{}/sites/{}/events".format(
        settings.OPENCLINICA_STUDY, settings.OPENCLINICA_SITE
    )
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)


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
    survey_member.survey_token = response.json()['accessCode']
    survey_member.save()


def send_user_survey_link(survey_member):
    url = settings.OPENCLINICA_PARTICIPATE_LINK + "?accessCode={}".format(survey_member.survey_token)
    survey_member.member.message(
        subject="Here's your survey link!",
        message="Please use this URL to fill out the survey: {}".format(url))
