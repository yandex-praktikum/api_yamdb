import datetime as dt

from rest_framework.exceptions import ValidationError


def validate_year(value):
    year = dt.date.today().year
    if not (value <= year):
        raise ValidationError('Проверьте год выпуска фильма!')
