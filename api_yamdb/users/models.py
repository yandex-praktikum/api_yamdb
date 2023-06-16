from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

CHOICES_ROLE = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN)
]


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        verbose_name='Адрес e-mail',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    userrole = models.CharField(
        verbose_name='Роль пользователя',
        choices=CHOICES_ROLE,
        default=USER,
        blank=True
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
        default='1234567890'
    )

    @property
    def is_user(self):
        return self.userrole == USER
    
    @property
    def is_moderator(self):
        return self.userrole == MODERATOR
    
    @property
    def is_admin(self):
        return self.userrole == ADMIN



    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
