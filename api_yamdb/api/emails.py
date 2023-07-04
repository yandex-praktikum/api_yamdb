from django.core.mail import send_mail


EMAIL_SUBJECT = 'Код подтверждения'
EMAIL_MESSAGE = 'Ваш код'
FROM_EMAIL = 'your_email@example.com'
RECIPIENT_LIST = ['recipient1@example.com', 'recipient2@example.com']


def send_virtual_email():
    send_mail(
        subject=EMAIL_SUBJECT,
        message=EMAIL_MESSAGE,
        from_email=FROM_EMAIL,
        recipient_list=RECIPIENT_LIST,
        fail_silently=False,
    )
