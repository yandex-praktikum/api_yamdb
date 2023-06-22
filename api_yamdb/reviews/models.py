from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import SlugValidator
from users.models import User

Titles = get_user_model()


class Categories(models.Model):
    validator_slug = SlugValidator()
    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Наименование категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
        validators=[validator_slug],
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def str(self) -> str:
        return self.name


class Genres(models.Model):
    validator_slug = SlugValidator()
    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
        validators=[validator_slug],
    )

    class Meta:
        ordering = ('name',)
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
        ordering = ('year',)
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
        ordering = ('genre',)
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'


class Reviews(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews_title',
        null=True,
        blank=False)
    title = models.ForeignKey(
        Titles,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews_title',
        null=True,
        blank=False)
    text = models.TextField()
    created = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True,
        null=True,
        blank=False)
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        validators=(
            MaxValueValidator(10),
            MinValueValidator(1)
        ),
        error_messages={'validators': 'Оценка от 1 до 10!'},
        null=True,
        blank=False)

    class Meta:
        verbose_name = 'Отзыв',
        verbose_name_plural = 'Отзывы',
        ordering = ('created',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.name


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews_comment',
        null=True,
        blank=False)
    review = models.ForeignKey(
        Reviews,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='reviews_comment',
        null=True,
        blank=False)
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
        null=True,
        blank=False)

    class Meta:
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии'
        ordering = ('created',)

    def __str__(self):
        return self.name
