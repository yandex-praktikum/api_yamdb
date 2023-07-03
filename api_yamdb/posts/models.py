from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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
    year = models.IntegerField(
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        verbose_name='Описание произведения'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles'
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
    score = models.SmallIntegerField(verbose_name='Рейтинг')

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
