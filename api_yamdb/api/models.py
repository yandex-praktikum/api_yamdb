from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import (CharField, CheckConstraint, EmailField, Q,
                              TextField)
from django.utils.translation import gettext_lazy as _

from .managers import APIUserManager

only_admin = Q(role='admin') & Q(is_staff=True)
only_not_admin = Q(role__in=('user', 'moderator')) & Q(is_staff=False)


class User(AbstractUser):
    CHOICES = (
        ('user', 'пользователь'),
        ('moderator', 'модератор'),
        ('admin', 'админ')
    )
    username = CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=True,
        help_text=_('Required. 150 characters or fewer. '
                    'Letters, digits and @/./+/-/_ only.'),
        validators=(AbstractUser.username_validator,),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = EmailField('Email', unique=True)
    role = CharField('Роль', default='user', max_length=9, choices=CHOICES)
    bio = TextField('Биография', blank=True)

    objects = APIUserManager()

    USERNAME_FIELD = 'id'

    class Meta(AbstractUser.Meta):
        constraints = (
            CheckConstraint(
                name='only-admin-must-be-staff',
                check=only_admin | only_not_admin
            ),
        )

    def __str__(self):
        return str(self.pk)


class Categories(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(verbose_name='URL', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Все категории'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}: {self.slug}'


class Genres(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    slug = models.SlugField(verbose_name='URL', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}: {self.slug}'


class Titles(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания',
        blank=True, null=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genres,
        verbose_name='Жанр',
        blank=True, null=True
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Категория',
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Все произведения'

    def __str__(self):
        return self.name
