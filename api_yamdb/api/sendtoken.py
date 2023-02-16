import random

from django.core.mail import send_mail


def make_token(username):
    code = random.randint(0, 10000000)
    username.confirmation_code = code
    username.save()

    send_mail("Регистрация на сайте",
              message=f"Код подтверждения: "
                      f"{code}",
              from_email='admin@yamdb.com',
              recipient_list=[username.email],
              )
