from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название категории')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'объект «Категория»'
        default_permissions = (
            'add', 'delete', 'view'
        )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название жанра')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'объект «Жанр»'
        default_permissions = (
            'add', 'delete', 'view'
        )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='Описание произведения')
    genres = models.ManyToManyField(
        Genre, through='TitleGenre',
        verbose_name='Жанры произведения'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        related_name='titles', verbose_name='Категория произведения'
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
