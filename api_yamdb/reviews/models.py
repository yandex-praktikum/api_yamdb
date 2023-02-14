from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
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
        null=True,
        unique=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'Пользователи'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="me_not_in_username"
            )
        ]
