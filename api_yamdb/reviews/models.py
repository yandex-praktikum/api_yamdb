from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ROLE_CHOICES = (
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER)
)
MAX_CHARACTERS = 20


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.SlugField(
        'Никнейм', unique=True, max_length=settings.MAXL_USERNAME,
    )
    email = models.EmailField(
        'Email адрес', unique=True, max_length=settings.MAXL_EMAIL,
    )
    role = models.CharField(
        'Роль', choices=ROLE_CHOICES, default=USER, max_length=20,
    )
    bio = models.TextField('Биография', blank=True)
    first_name = models.CharField(
        'Имя', max_length=settings.MAXL_NAME, blank=True,
    )
    last_name = models.CharField(
        'Фамилия', max_length=settings.MAXL_NAME, blank=True,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:MAX_CHARACTERS]


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField('Имя категории', max_length=settings.MAXL_NAME)
    slug = models.SlugField(
        'Слаг', unique=True, max_length=settings.MAXL_SLUG,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:MAX_CHARACTERS]


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField('Имя жанра', max_length=settings.MAXL_NAME)
    slug = models.SlugField('Слаг', max_length=settings.MAXL_SLUG)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:MAX_CHARACTERS]


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField('Название', max_length=settings.MAXL_NAME)
    year = models.DateField('Год выпуска')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre, related_name='titles', verbose_name='Жанры',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:MAX_CHARACTERS]
