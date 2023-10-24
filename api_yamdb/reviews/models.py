from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

TEXT_LIM = 15


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание')
    genre = models.ManyToManyField('Genre',
                                   through='Partnership',
                                   through_fields=('name', 'genre'),
                                   related_name='titles',
                                   verbose_name='Slug жанра'
                                   )
    category = models.OneToOneField('Category',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name='titles',
                                    verbose_name='Slug категории'
                                    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'

    def __str__(self):
        return self.name[:TEXT_LIM]


class BaseModel(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            help_text='Идентификатор страницы для URL; '
                                      'разрешены символы латиницы, '
                                      'цифры, дефис и подчёркивание.',
                            verbose_name='Slug'
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


class Partnership(models.Model):
    name = models.ForeignKey(Title, on_delete=models.DO_NOTHING)
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
