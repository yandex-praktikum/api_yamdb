from datetime import datetime

from django.core.validators import MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='URL slug',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='URL slug',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[MaxValueValidator(datetime.now().year)],
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='catigories',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
