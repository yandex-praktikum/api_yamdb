from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError


def validate_year(value):
    dt = datetime.now().year
    dl = len(value)
    if value > dt or dl < 0:
        raise ValidationError(
            ('Проверьте ещё раз год'),
            params={value},
        )


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    description = models.TextField('Описание')
    year = models.IntegerField(validators=[validate_year])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=False,
        verbose_name="Категория"
    )
    genre = models.ManyToManyField(
        Genre, on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name="Жанр"
    )

    def __str__(self):
        return self.name
