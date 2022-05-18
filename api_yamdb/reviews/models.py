from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from users.models import User


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


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва',
                            help_text='Введите текст отзыва')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Автор отзыва')
    score = models.IntegerField(default=1,
                                validators=[MaxValueValidator(10),
                                            MinValueValidator(1)],
                                help_text='Оценка 1 до 10',
                                verbose_name='Оценка')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации',)
    title = models.ForeignKey(Title,
                                  on_delete=models.CASCADE,
                                  related_name='reviews',
                                  verbose_name='Произведение')

    class Meta:
        unique_together = ['author', 'title']
        # Пользователь может оставить только один отзыв на произведение.
        ordering = ['-pub_date']  # Порядок по умолчанию
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self) -> str:
        return self.text[:20]


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               verbose_name='Отзыв',
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(verbose_name='Текст комментария',
                            help_text='Введите текст комментария')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор комментария')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации',)

    class Meta:
        ordering = ['-pub_date']  # Порядок по умолчанию
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return f'Комментарий от {self.author} к {self.review}'
