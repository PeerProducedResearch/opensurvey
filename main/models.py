from django.db import models
from openhumans.models import OpenHumansMember


class SurveyAccount(models.Model):
    """
    Store additional data for an Open humans member.
    This is a one to one relationship with a OpenHumansMember object.
    """

    member = models.OneToOneField(OpenHumansMember, on_delete=models.CASCADE)
    survey_token = models.TextField(blank=True, null=True)
