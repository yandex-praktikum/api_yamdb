from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = ['email']
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name='Name'
    )
    email = models.EmailField(
        max_length=254, unique=True, blank=False, verbose_name='Email адресс'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Clearance level',
    )
    bio = models.TextField(max_length=100, blank=True, verbose_name='About me')
    confirmation_code = models.CharField(
        max_length=70, unique=True, blank=True, null=True
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('id',)
