from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()
Titles = get_user_model()


class Review(models.Model):
    author = models.ForeignKey(
        'Автор',
        User,
        on_delete=models.CASCADE,
        related_name='reviews')
    title = models.ForeignKey(
        'Произведение',
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)
    rating = models.IntegerField(
        'Рейтинг',
        validators=(
            MaxValueValidator(10),
            MinValueValidator(1)
            ),
        error_messages={'validators': 'Оценка от 1 до 10!'}
        )


class Comment(models.Model):
    author = models.ForeignKey(
        'Автор',
        User,
        on_delete=models.CASCADE,
        related_name='reviews')
    review = models.ForeignKey(
        'Отзыв',
        Review,
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)
