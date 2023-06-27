from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import UsernameValidator

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

CHOICES_ROLE = [(USER, USER),
                (MODERATOR, MODERATOR),
                (ADMIN, ADMIN)]


class User(AbstractUser):
    validator_username = UsernameValidator()
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[validator_username],
    )
    email = models.EmailField(
        verbose_name='Адрес e-mail',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        verbose_name='Имя', max_length=150, blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=150, blank=True
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=15,
        choices=CHOICES_ROLE,
        default=USER,
        blank=True,
    )
    bio = models.CharField(
        verbose_name='Краткая биография',
        max_length=254,
        blank=True,
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=254,
        null=True,
        blank=False,
        default='1234567890',
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
