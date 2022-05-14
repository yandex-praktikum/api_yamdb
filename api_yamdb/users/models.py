from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES_CHOICES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    )

    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(verbose_name='first name',
                                  max_length=150, blank=True)
    email = models.EmailField(max_length=254,
                              verbose_name='Адрес электронной почты',
                              unique=True)
    bio = models.TextField(verbose_name='О себе',
                           null=True,
                           blank=True)
    role = models.CharField(verbose_name='Роль',
                            max_length=20,
                            choices=ROLES_CHOICES, default=USER)

    def is_moderator(self):
        return self.role in self.MODERATOR

    def is_admin(self):
        return self.role in self.ADMIN

    USERNAME_FIELD = 'email'   # Строка, описывающая имя поля в
    # пользовательской модели, которое используется
    # в качестве уникального идентификатора
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
