from django.db import models
# from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import User
from django_filters import rest_framework as filters


def validate_even(value):
    if value > timezone.now().year:
        raise ValidationError((' %(value)s назад в будущее!'),
                              params={'value': value},)


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Категория')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Жанр')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):

    name = models.CharField(max_length=200,
                            verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Год выпуска',
                               validators=[validate_even])

    rating = models.IntegerField(null=True, verbose_name='Рейтинг')
#  нужен ли он тут или его реализуем в view?
    description = models.TextField(verbose_name='Описание',
                                   null=True, blank=True)
    genre = models.ManyToManyField(Genre, related_name='titles',
                                   verbose_name='Жанр')
    category = models.ForeignKey(Category, related_name='titles',
                                 on_delete=models.DO_NOTHING,
                                 verbose_name='Категория',)

    class Meta:
        verbose_name = 'Название произведения'
        verbose_name_plural = 'Названия произведений'


class TitletFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    genre = filters.CharFilter(field_name="genre__slug", lookup_expr='exact')
    category = filters.CharFilter(field_name="category__slug",
                                  lookup_expr='exact')
    year = filters.NumberFilter(field_name='year', lookup_expr='icontains')

    class Meta:

        model = Title
        fields = ['name', 'category', 'genre', 'year']


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = ["title", "author"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )

    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.ForeignKey, related_name="comments"
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["id"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
