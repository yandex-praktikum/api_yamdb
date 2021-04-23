from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name[:100]


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name[:100]


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    category = models.ForeignKey(Category,  
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 related_name="title")
    description = models.TextField( blank=True)
    def __str__(self):
        return self.name       