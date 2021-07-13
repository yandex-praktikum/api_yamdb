from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('User', 'user'),
        ('Moderator', 'moderator'),
        ('Admin', 'admin')
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='User')
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