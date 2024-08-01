from django.contrib.auth.models import AnonymousUser
from django.middleware.locale import LocaleMiddleware as BasedMiddleware
from django.utils import translation
from django.conf import settings

from weather.utils.translation import get_language_from_user


class LocaleMiddleware(BasedMiddleware):
    def process_request(self, request):
        if request.user.is_anonymous:
            return
        lang_code = get_language_from_user(request, request.user)
        if lang_code is None:
            lang_code = settings.LANGUAGE_CODE

        translation.activate(language=lang_code)
        request.LANGUAGE_CODE = translation.get_language()

        