from django.conf import settings
import requests
import json

def create_openclinica_user(survey_member):
    headers = {
        "Authorization": "bearer {}".format(settings.OPENCLINICA_TOKEN),
        "Content-Type": "application/json"
    }
    data = {
        "identifier": survey_member.member.oh_id,
        "subjectKey": survey_member.member.oh_id
        }
    url = "https://opencovid.openclinica.io/OpenClinica/pages/auth/api/clinicaldata/studies/{}/sites/{}/participants?register=y".format(
        settings.OPENCLINICA_STUDY, settings.OPENCLINICA_SITE
    )
    print(url)
    print(data)
    print(headers)

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
