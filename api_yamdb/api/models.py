from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('User', 'user'),
        ('Moderator', 'moderator'),
        ('Admin', 'admin')
    )
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='User'
    )
    description = models.TextField(max_length=500, blank=True)
    confirmation_code = models.IntegerField(default=0)



class Genres(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Адрес', unique=True)    

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name  


class Categories(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Адрес', unique=True)    

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name         


class Titles(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.CharField('Год выпуска', max_length=200)
    description = models.TextField('Описание')
    genre = models.ManyToManyField(Genres, related_name='titles', blank=True, null=True,
                                    verbose_name='Жанр')
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                related_name='titles', blank=True, null=True,
                                verbose_name='Категория')                          

    def __str__(self):
        return self.name    

class Review(models.Model):
    RATING_LEVELS = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
    )

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    text = models.TextField(verbose_name='Текст', max_length=5000)
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(verbose_name='Рейтинг', choices=RATING_LEVELS)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.text
