from django.db import models

from core.models import NameSlugBaseModel


class Category(NameSlugBaseModel):

    class Meta:
        verbose_name = 'объект «Категория»'


class Genre(NameSlugBaseModel):

    class Meta:
        verbose_name = 'объект «Жанр»'


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='Описание произведения')
    genre = models.ManyToManyField(
        Genre, through='TitleGenre',
        verbose_name='Жанры произведения'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        related_name='titles',
        #related_name='category',
        verbose_name='Категория произведения'
    )

    class Meta:
        verbose_name = 'объект «Произведение»'
        default_permissions = (
            'add', 'change', 'delete', 'view'
        )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.SET_NULL,
                              related_name='titles',
                              null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              related_name='genres',
                              null=True)

    def __str__(self):
        return f'{self.title} {self.genre}'
