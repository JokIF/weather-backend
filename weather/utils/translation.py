from django.utils.translation import get_supported_language_variant, check_for_language
from django.utils.translation.trans_real import parse_accept_lang_header, get_languages, language_code_re
from django.conf import settings


def get_language_from_user(request, user):
    lang_code = user.get_language()
    if (
        lang_code is not None
        and lang_code in get_languages()
        and check_for_language(lang_code)
    ):
        return lang_code

    try:
        return get_supported_language_variant(lang_code)
    except LookupError:
        pass

    accept = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
    for accept_lang, unused in parse_accept_lang_header(accept):
        if accept_lang == "*":
            break

        if not language_code_re.search(accept_lang):
            continue

        try:
            return get_supported_language_variant(accept_lang)
        except LookupError:
            continue

    try:
        return get_supported_language_variant(settings.LANGUAGE_CODE)
    except LookupError:
        return settings.LANGUAGE_CODE
