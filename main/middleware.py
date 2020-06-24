from django.conf import settings
from django.utils import translation

import logging
logger = logging.getLogger(__name__)


class LoginLangMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            current_language = translation.get_language()
            saved_language = request.user.openhumansmember.surveyaccount.language
            if saved_language != current_language and saved_language in [lang[0] for lang in settings.LANGUAGES]:
                response.set_cookie(
                    settings.LANGUAGE_COOKIE_NAME, saved_language,
                    max_age=settings.LANGUAGE_COOKIE_AGE,
                    path=settings.LANGUAGE_COOKIE_PATH,
                    domain=settings.LANGUAGE_COOKIE_DOMAIN,
                    secure=settings.LANGUAGE_COOKIE_SECURE,
                    httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                    samesite=settings.LANGUAGE_COOKIE_SAMESITE,
                )

        return response
