from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

roles = [
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
]


class CostumUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=9, choices=roles, default='user')
    description = models.CharField('bio', max_length=500)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
