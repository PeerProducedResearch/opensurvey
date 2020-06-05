from django.core.management.base import BaseCommand
import requests
from main.helpers import get_access_token


class Command(BaseCommand):
    help = "Exports data for all members"

    def handle(self, *args, **options):
        headers = {
            "Authorization": "bearer {}".format(get_access_token(download=True)),
            "Accept": "application/json"
            }
        url = "https://opencovid.openclinica.io/OpenClinica/pages/auth/api/clinicaldata/S_DEMO_BGT(TEST)/91048557/*/*?includeAudits=n&includeDNs=n&includeMetadata=y&showArchived=n"
        # download all data:
        # url = "https://opencovid.openclinica.io/OpenClinica/pages/auth/api/clinicaldata/S_DEMO_BGT(TEST)/*/*/*?includeAudits=n&includeDNs=n&includeMetadata=y&showArchived=n"
        response = requests.get(url, headers=headers)
        print(response.json())

        # TODO: so far it doesn't process the data, next step:
        # - Save data to Open Humans for each member
