from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone


def get_current_year():
    return timezone.now().year


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=256
    )
    slug = models.SlugField(
        'Слаг категории',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('slug',)

    def __str__(self):
        return {self.name}


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        'Слаг жанра',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('slug',)

    def __str__(self):
        return {self.name}


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=256
    )
    year = models.IntegerField(
        'Год издания',
        validators=[MaxValueValidator(get_current_year)],
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        db_index=True
    )
    description = models.TextField(
        'Описание произведения',
        max_length=256,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='жанр',
        db_index=True
    )
    rating = models.FloatField(
        default=None,
        null=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        'Genre', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        'Title', on_delete=models.CASCADE, verbose_name='Произведение'
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return f"{self.genre} {self.title}"
