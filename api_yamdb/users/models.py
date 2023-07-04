from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import username_validation


class User(AbstractUser):
    """Создание кастомной модели пользователя."""
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    username = models.CharField(
        unique=True,
        max_length=150,
        validators=(username_validation,),
        verbose_name='Никнейм пользователя',
        help_text='Введите никнейм'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='e-mail'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пользователя',
        help_text='Введите фамилию'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        help_text='Введите имя'
    )
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        choices=settings.ROLES, default=USER
    )

    class Meta:
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username
