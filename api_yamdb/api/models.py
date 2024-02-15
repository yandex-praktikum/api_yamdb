from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
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
        default='user'
    )
    bio = models.TextField('Биография')
    first_name = models.CharField('Имя пользователя', max_length=50)
    last_name = models.CharField('Фамилия пользователя', max_length=50)
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
