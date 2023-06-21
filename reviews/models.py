from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()
Titles = get_user_model()


class Reviews(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=False)
    title = models.ForeignKey(
        Titles,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
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
        blank=False
        )

    class Meta:
        verbose_name = 'Отзывы',
        ordering = ('created')
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
        related_name='reviews',
        null=True,
        blank=False)
    review = models.ForeignKey(
        Reviews,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='reviews',
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
        verbose_name = 'Комментарии',
        ordering = ('created')

    def __str__(self):
        return self.name
