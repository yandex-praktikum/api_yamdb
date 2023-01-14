# api/utils.py

import secrets
import string

from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_code(user):
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {user.confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )


def get_confirmation_code():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break

    return password
