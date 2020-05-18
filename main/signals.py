from django.db.models.signals import post_save
from django.dispatch import receiver
from openhumans.models import OpenHumansMember
from .models import SurveyAccount
from .helpers import create_openclinica_user, create_openclinica_event, get_openclinica_token, send_user_survey_link
import datetime

@receiver(post_save, sender=OpenHumansMember)
def my_handler(sender, instance, created, **kwargs):
    if created:
        survey_account = SurveyAccount.objects.create(
            member=instance
        )
        survey_account.save()
        create_openclinica_user(survey_account)
        create_openclinica_event(survey_account, "SE_FSFD", str(datetime.date.today()))
        get_openclinica_token(survey_account)
        send_user_survey_link(survey_account)
