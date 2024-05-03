import random

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.forms import ValidationError

USER_ROLES_CHOICES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)

USERNAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254


class YamdbUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': ('Пользователь с таким именем уже существует!'),
        },
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        error_messages={
            'unique': (
                'Пользователь с такой электронной почтой уже существует!'),
        },
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя',
        max_length=9,
        choices=USER_ROLES_CHOICES,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=5,
        blank=True
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['pk']

    def clean(self):
        super().clean()
        if self.username == 'me':
            raise ValidationError(
                'Запрещено использовать "me" как имя пользователя!')

    def send_confirmation_email(self):
        confirmation_code = random.randint(10000, 99999)
        self.confirmation_code = confirmation_code
        self.save()

        send_mail(
            'Код подтверждения',
            (f'Привет, {self.username}!\n'
             f'Ваш код подтверждения: {self.confirmation_code}'),
            'from@example.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.username
