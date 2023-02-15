from django.db import models
from django.contrib.auth.models import AbstractUser

from api.utils import generate
from .titles import Title

RATE_CHOICES = [(i) for i in range(11)]


class User(AbstractUser):
    """ Модель пользователя """

    USER = 'User'
    MODERATOR = 'Moderator'
    ADMIN = 'Admin'

    ROLES = (
        ('AD', USER),
        ('MOD', MODERATOR),
        ('US', USER)
    )

    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=9,
        choices=ROLES,
        default=USER,
        verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=50,
        default=generate(),
        verbose_name='Код подтверждения'
    )
    email = models.EmailField(
        max_length=128,
        unique=True,
        verbose_name='Email'
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique username and email'
            )
        ]


class Rating(models.Model):
    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('author', 'title')
        verbose_name = 'Оценка'
        ordering = ['rating']

    def average_rating(self):
        all_ratings = list(map(lambda x: x.value, self.reviews.all()))
        sum_all_ratings = sum(all_ratings)
        return (round(sum_all_ratings / len(all_ratings), 0))

    def __str__(self):
        return self.rating


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.ForeignKey(
        Rating, default=0, null=True, blank=True)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    slug = models.SlugField(unique=True)

    class Meta:
        unique_together = ('author', 'title')
        verbose_name = 'Отзыв'
        ordering = ['reviews']

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
