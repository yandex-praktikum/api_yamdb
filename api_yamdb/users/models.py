from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
SUPERUSER = 'superuser'

CHOICES_ROLE = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
    (SUPERUSER, SUPERUSER),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    userrole = models.CharField(
        'роль пользователя',
        max_length=10,
        choices=CHOICES_ROLE,
        default=USER,
        blank=True
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    @property
    def is_user(self):
        return self.userrole == USER
    
    @property
    def is_moderator(self):
        return self.userrole == MODERATOR
    
    @property
    def is_admin(self):
        return self.userrole == ADMIN or self.userrole ==SUPERUSER



    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
