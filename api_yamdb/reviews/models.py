from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Наименование категории'
    )
    slug = models.SlugField(
        unique=True,
        blank=False
    )

    class Meta:
        # ordering = (-'name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def str(self) -> str:
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        blank=False
    )

    class Meta:
        # ordering = (-'name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def str(self) -> str:
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        # max_length=4,
        blank=False,
        verbose_name='Год создания произведения'
    )
    category = models.ForeignKey(
        Categories,
        blank=False,
        null=True,
        related_name='titles',
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,

    )
    genre = models.ManyToManyField(
        Genres,
        through='TitleGenre',
        blank=False,
        verbose_name='Описание жанра'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание произведения'
    )

    class Meta:
        # ordering = (-'year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def str(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE
    )

    class Meta:
        # ordering = (-'genre',)
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'
