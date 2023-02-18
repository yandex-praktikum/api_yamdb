from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        null=True,
        blank=True,
    )
    role = models.CharField(
        'Роль пользователя',
        blank=True,
        max_length=100,
        choices=ROLES,
        default=USER,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        null=True,
        unique=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'Пользователи'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="me_not_in_username"
            )
        ]


class Genre(models.Model):
    """Жанр произведения. Содержит название и slug"""
    name = models.CharField(verbose_name='Название жанра', max_length=256)
    slug = models.SlugField(verbose_name='Slug имя жанра',
                            max_length=50,
                            unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория (тип) произведения. Например, 'фильм', 'книга' """
    name = models.CharField(verbose_name='Название категории', max_length=256)
    slug = models.SlugField(verbose_name='Slug имя категории',
                            max_length=50,
                            unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение"""
    name = models.CharField(verbose_name='Название произведения',
                            max_length=256)
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска произведения')
    description = models.TextField(verbose_name='Описание произведения',
                                   blank=True)
    # у категории изменить поведение on_delete, вероятно ставить null
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='titles')
    genre = models.ManyToManyField(Genre, related_name='titles',
                                   through='TitleGenre')

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name="titles",
                              verbose_name="Произведение",)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              related_name='genres',
                              verbose_name="Жанр")

    def __str__(self) -> str:
        return f'{self.title} : {self.genre}'
