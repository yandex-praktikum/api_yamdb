import re

from rest_framework.serializers import ValidationError

FORBIDDEN_SYMBOLS=r'^[\w.@+-]+\Z'

def username_validation(value):
    """Валидатор для проверки введенного имени пользователя."""
    checked_value = re.compile(FORBIDDEN_SYMBOLS, value)
    if checked_value:
        raise ValidationError('Запрещенные символы в username!')
    return value
