from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
)


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^([-\w]+)$',
                message=' Letters, digits and @/./+/-/_ only.',
            ),
        ]
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254
    )
    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )
    bio = models.TextField('Биография')
    role = models.CharField(
        'Роль',
        choices=CHOICES,
        default='user',
        max_length=150
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]
