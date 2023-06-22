from django.core.validators import RegexValidator

from api_yamdb.settings import REGEX_SLUG


class SlugValidator(RegexValidator):
    regex = REGEX_SLUG
