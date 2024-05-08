from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.forms import ValidationError

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from core import constants as const


class YamdbUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        'Имя пользователя',
        max_length=const.USERNAME_MAX_LENGTH,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': ('Пользователь с таким именем уже существует!'),
        },
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=const.EMAIL_MAX_LENGTH,
        unique=True,
        error_messages={
            'unique': (
                'Пользователь с такой электронной почтой уже существует!'),
        },
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя',
        max_length=const.ROLE_MAX_LENGTH,
        choices=const.USER_ROLES_CHOICES,
        default=const.USER
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['username']

    def clean(self):
        super().clean()
        if self.username == 'me':
            raise ValidationError(
                'Запрещено использовать "me" как имя пользователя!')

    def send_confirmation_email(self, user):
        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='Код подтверждения',
            message=(f'Привет, {self.username}!\n'
                     f'Ваш код подтверждения: {confirmation_code}'),
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            fail_silently=False,
        )

    @property
    def is_admin(self):
        return self.role == const.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == const.MODERATOR

    def __str__(self):
        return self.username
