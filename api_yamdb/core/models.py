from django.db import models

from core import constants as const

class NameSlugBaseModel(models.Model):
    name = models.CharField(max_length=const.MAX_LENGTH_NAME_FIELD,
                            verbose_name='Название')
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг')

    class Meta:
        abstract = True
        ordering = ('name',)
        default_permissions = (
            'add', 'delete', 'view'
        )

    def __str__(self):
        return self.name
