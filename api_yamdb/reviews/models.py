import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


def today_year():
    return int(datetime.date.today().year)


class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Жанр')
    slug = models.SlugField(
        blank=True, unique=True, verbose_name='Адрес жанра'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Категория')
    slug = models.SlugField(
        max_length=50, blank=True, unique=True, verbose_name='Адрес категории'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        unique=True, max_length=255, verbose_name='Произведение'
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        db_index=True,
        validators=[MaxValueValidator(today_year())],
        verbose_name='Год выпуска',
    )
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre, blank=True, related_name='titles', verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )

    def genre_for_admin(self):
        result = '(None)'
        if self.genre.exists():
            result = self.genre.values_list('name', flat=True)
        return result

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    text = models.TextField(null=False, verbose_name='Отзыв')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Оценка',
    )

    class Meta:
        unique_together = ['author', 'title']
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.id}'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    text = models.TextField(verbose_name='Комментарий')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        ordering = ['-pub_date']
