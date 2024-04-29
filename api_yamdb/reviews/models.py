from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import YamdbUser


# Можно добавить BaseModel в соседний файл
# И наследовать в категориях и жанрах от него
# class NameSlugBaseModel(models.Model):
# class Meta:// abstract = True
class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название категории')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'объект «Категория»'
        default_permissions = (
            'add', 'delete', 'view'
        )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название жанра')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'объект «Жанр»'
        default_permissions = (
            'add', 'delete', 'view'
        )

    def __str__(self):
        return self.name


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


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.SET_NULL,
                              related_name='titles',
                              null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL,
                              related_name='genres',
                              null=True)

    def __str__(self):
        return f'{self.title} {self.genre}'


# Надо не забыть создать миграции для отзывов
# Сейчас пока не работают миграции
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
