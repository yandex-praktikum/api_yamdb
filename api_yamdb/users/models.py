import random

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.forms import ValidationError

USER_ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class YamdbUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': ('Пользователь с таким именем уже существует.'),
        },
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        error_messages={
            'unique': (
                'Пользователь с такой электронной почтой уже существует.'),
        },
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя',
        max_length=16,
        choices=USER_ROLES,
        default='user'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=16,
        blank=False,
        default=random.randint(1000, 9999))

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['pk']

    def clean(self):
        super().clean()
        if self.username == 'me':
            raise ValidationError(
                'Запрещено использовать "me" как имя пользователя.')

    def __str__(self):
        return self.username
