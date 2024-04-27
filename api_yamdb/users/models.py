from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ValidationError

USER_ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class YamdbUser(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль пользователя',
        max_length=16,
        choices=USER_ROLES,
        default='user'
    )

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
