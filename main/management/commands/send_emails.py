from django.core.management.base import BaseCommand
from main.models import SurveyAccount
import datetime
from main.helpers import create_openclinica_event, get_openclinica_token
from main.helpers import send_user_survey_link

class Command(BaseCommand):
    help = "Updates all data for all members"

    def handle(self, *args, **options):
        for survey_account in SurveyAccount.objects.all():
            #create_openclinica_event(survey_account, "SE_DAILY", str(datetime.date.today()))
            get_openclinica_token(survey_account)
            send_user_survey_link(survey_account)
