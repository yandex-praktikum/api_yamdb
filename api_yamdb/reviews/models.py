import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()

TEXT_LIM = 15


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.PositiveSmallIntegerField('Год выпуска')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField('Genre',
                                   related_name='titles',
                                   verbose_name='Slug жанра'
                                   )
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='titles',
                                 verbose_name='Slug категории'
                                 )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.CheckConstraint(
                check=models.Q(year__gte=1000)
                & models.Q(year__lte=dt.date.today().year),
                name='A year value is valid between 1000 and year_now',
            )
        ]

    def __str__(self):
        return self.name[:TEXT_LIM]


class BaseModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            help_text='Идентификатор страницы для URL; '
                                      'разрешены символы латиницы, '
                                      'цифры, дефис и подчёркивание.',
                            verbose_name='Slug',
                            validators=[RegexValidator(
                                regex=r'^[-a-zA-Z0-9_]+$',
                                message='Идентификатор страницы для URL '
                                        'должен содержать только символы '
                                        'латиницы, цифры, дефис '
                                        'и подчёркивание.'
                            ),
                            ]
                            )

    class Meta:
        ordering = ('name',)
        abstract = True

    def __str__(self):
        return self.name


class Genre(BaseModel):

    class Meta:
        verbose_name = 'Slug жанра'
        verbose_name_plural = 'Slug жанров'


class Category(BaseModel):

    class Meta:
        verbose_name = 'Slug категории'
        verbose_name_plural = 'Slug категорий'
