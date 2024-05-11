import datetime as dt

from django.core.exceptions import ValidationError

from core import constants as const


def validate_year(value):
    current_year = dt.datetime.today().year
    if not (value <= current_year):
         raise ValidationError(message=const.MESSAGE_VALIDATION_YEAR_ERROR)
