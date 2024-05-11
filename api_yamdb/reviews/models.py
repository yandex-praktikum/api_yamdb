from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from django.db import models

from core import constants as const
from core.models import NameSlugBaseModel, ReviewCommentBaseModel

from .validators import validate_year

User = get_user_model()


class Category(NameSlugBaseModel):

    class Meta:
        verbose_name = 'объект «Категория»'
        verbose_name_plural = 'объекты «Категорий»'


class Genre(NameSlugBaseModel):

    class Meta:
        verbose_name = 'объект «Жанр»'
        verbose_name_plural = 'объекты «Жанров»'


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.PositiveSmallIntegerField(validators=[validate_year],
                                            verbose_name='Год выпуска')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание произведения')
    genre = models.ManyToManyField(
        Genre, through='TitleGenre',
        verbose_name='Жанры произведения'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        related_name='titles',
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
                              related_name='titlesgenres',
                              null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              related_name='titlesgenres',
                              null=True)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(ReviewCommentBaseModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название произведения',
        related_name='reviews'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='reviews')
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                const.MIN_SCORE,
                f'Значение рейтинга должно быть больше {const.MIN_SCORE}.'),
            MaxValueValidator(
                const.MAX_SCORE,
                f'Значение рейтинга должно быть меньше {const.MAX_SCORE}.')],
        verbose_name='Рейтинг')

    class Meta(ReviewCommentBaseModel.Meta):
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_author_title')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(ReviewCommentBaseModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Комментарии',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
    )

    class Meta(ReviewCommentBaseModel.Meta):
        verbose_name = 'Комментарий'
