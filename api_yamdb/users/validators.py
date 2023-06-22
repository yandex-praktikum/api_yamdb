from django.core.validators import RegexValidator

from api_yamdb.settings import REGEX_STR


class UsernameValidator(RegexValidator):
    regex = REGEX_STR
