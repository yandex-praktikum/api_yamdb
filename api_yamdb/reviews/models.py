from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    """Модель отзывов к произведениям."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name='Рейтинг произведения'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )
    slug = models.SlugField(unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='Одно произведение- один отзыв одному автору'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев к отзывам."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
