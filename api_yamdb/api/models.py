from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

USER_ROLE = 'user'
MODERATOR_ROLE = 'moderator'
ADMIN_ROLE = 'admin'


class User(AbstractUser):
    is_user = False
    is_moderator = False
    is_admin = False

    ROLE_CHOICES = (
        (USER_ROLE, 'User'),
        (MODERATOR_ROLE, 'Moderator'),
        (ADMIN_ROLE, 'Admin')
    )
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=USER_ROLE
    )
    bio = models.TextField(blank=True)
    confirmation_code = models.IntegerField(default=0)
    email = models.EmailField(_('email address'), unique=True)

    class Meta:
        ordering = ['-username']

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        if self.role == USER_ROLE:
            return True

    @property
    def is_moderator(self):
        if self.role == MODERATOR_ROLE:
            return True

    @property
    def is_admin(self):
        if self.role == ADMIN_ROLE:
            return True


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
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание')
    genre = models.ManyToManyField(Genres, related_name='titles', blank=True,
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


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField(verbose_name='Текст комментария', max_length=450)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text
