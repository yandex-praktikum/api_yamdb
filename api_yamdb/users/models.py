from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )

    username = models.CharField(
        'usermane',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=50,
        choices=ROLES,
        default='user'
    )
    bio = models.TextField('Биография', blank=True)
    first_name = models.CharField(
        'Имя пользователя',
        max_length=50,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=50,
        blank=True
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
