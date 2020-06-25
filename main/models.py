from django.db import models
from openhumans.models import OpenHumansMember
import secrets
import datetime
from django.utils.timezone import now


class SurveyAccount(models.Model):
    """
    Store additional data for an Open humans member.
    This is a one to one relationship with a OpenHumansMember object.
    """

    member = models.OneToOneField(OpenHumansMember, on_delete=models.CASCADE)
    survey_token = models.TextField(blank=True, null=True)
    last_survey = models.DateField(blank=True, null=True)
    last_email = models.DateField(blank=True, null=True)
    consent_given = models.BooleanField(default=False)
    language = models.CharField(max_length=5, default='en')


TOKEN_EXPIRATION_MINUTES = 1440  # default expiration is one day


def create_token():
    return secrets.token_urlsafe(16)


class ReportToken(models.Model):
    member = models.ForeignKey(OpenHumansMember, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    token = models.TextField(default=create_token)
    minutes_valid = models.IntegerField(default=TOKEN_EXPIRATION_MINUTES)

    def is_valid(self):
        expires = self.created + datetime.timedelta(minutes=self.minutes_valid)
        if expires > now():
            return True
        return False

    def valid_member(self):
        if self.is_valid():
            return self.member
        return None
