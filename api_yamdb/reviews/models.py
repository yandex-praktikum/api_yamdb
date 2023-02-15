from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import validate_regex


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        null=True,
        blank=True,
    )
    role = models.CharField(
        'Роль пользователя',
        blank=True,
        max_length=100,
        choices=ROLES,
        default=USER,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[validate_regex]
    )
    confirmation_code = models.CharField(
        'Код авторизации',
        max_length=10000000,
        blank=True,
        null=True
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'Пользователи'
