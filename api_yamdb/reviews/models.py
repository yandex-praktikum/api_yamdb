from django.db import models
from django.contrib.auth.models import AbstractUser

from api.utils import generate


class User(AbstractUser):
    """ Модель пользователя """

    USER = 'User'
    MODERATOR = 'Moderator'
    ADMIN = 'Admin'

    ROLES = (
        ('AD', USER),
        ('MOD', MODERATOR),
        ('US', USER)
    )

    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=9,
        choices=ROLES,
        default=USER,
        verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=50,
        default=generate(),
        verbose_name='Код подтверждения'
    )
    email = models.EmailField(
        max_length=128,
        unique=True,
        verbose_name='Email'
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique username and email'
            )
        ]
