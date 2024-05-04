from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import YamdbUser
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
        # related_name='category',
        verbose_name='Категория произведения'
    )

    class Meta:
        verbose_name = 'объект «Произведение»'
        default_permissions = (
            'add', 'change', 'delete', 'view'
        )

    def __str__(self):
        return self.name

class Review(models.Model):
    text = models.TextField(verbose_name='текст отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название произведения'
    )

    author = models.ForeignKey(
        YamdbUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='reviews')
    score = models.PositiveSmallIntegerField(
        default=10,
        validators=[
            MinValueValidator(
                1, 'Значение рейтинга должно быть больше 1.'),
            MaxValueValidator(
                10, 'Значение рейтинга должно быть меньше 10.')],
        verbose_name='Рейтинг')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации отзыва'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_author_title')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
<<<<<<< HEAD
        return f'{self.title} {self.genre}'


class Review(models.Model):
    text = models.TextField(verbose_name='текст отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название произведения'
    )

    author = models.ForeignKey(
        YamdbUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='reviews')
    score = models.PositiveSmallIntegerField(
        default=10,
        validators=[
            MinValueValidator(
                1, 'Значение рейтинга должно быть больше 1.'),
            MaxValueValidator(
                10, 'Значение рейтинга должно быть меньше 10.')],
        verbose_name='Рейтинг')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации отзыва'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_author_title')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
=======
>>>>>>> develop
        # в модель YamdbUser нужно добавить поле username
        return f'Отзыв {self.author.username} на {self.title.name}'


class Comment(models.Model):
    text = models.TextField(verbose_name='text')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Комментарии',
        related_name='comments'
    )
    author = models.ForeignKey(
        YamdbUser,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
        null=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
