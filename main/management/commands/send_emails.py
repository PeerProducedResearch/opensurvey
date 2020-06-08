from django.core.management.base import BaseCommand
from main.models import SurveyAccount
from main.helpers import get_openclinica_token
from main.helpers import send_user_survey_link


class Command(BaseCommand):
    help = "Updates all data for all members"

    def handle(self, *args, **options):
        for survey_account in SurveyAccount.objects.filter(consent_given=True):
            # we no longer create events on sending out email, it's dynamically
            # done when clicking the email link now
            # create_openclinica_event(survey_account, "SE_DAILY", str(datetime.date.today()))
            get_openclinica_token(survey_account)
            send_user_survey_link(survey_account)
