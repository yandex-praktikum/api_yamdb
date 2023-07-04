import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    """Описание модели категорий произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Адрес категории (уникальный)'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Описание модели категории жанров."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Адрес жанра (уникальный)'
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Описание модели произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[MinValueValidator(
            limit_value=1,
            message='Год не может быть меньше или равен нулю'),
            MaxValueValidator(
                limit_value=dt.date.today().year,
                message='Год не может быть больше текущего года')],
    )
    description = models.TextField(
        verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles'
    )

    def __str__(self):
        return self.name
    

class Review(models.Model):
    """Описание модели отзыва."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField()
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.SmallIntegerField(
        verbose_name='Рейтинг',
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title_id'],
                                    name='unique_review_for_title')
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Описание модели комментария."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()

    def __str__(self):
        return self.text[:15]
