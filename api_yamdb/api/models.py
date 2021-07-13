from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('User', 'user'),
        ('Moderator', 'moderator'),
        ('Admin', 'admin')
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='User')
    description = models.TextField(max_length=500, blank=True)
