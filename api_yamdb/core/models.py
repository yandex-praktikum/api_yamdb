from django.db import models


class NameSlugBaseModel(models.Model):
    """
    Абстрактная модель.
    Добавляет к модели поля название и слаг.
    Ограничивает набор допустимых запросов.
    Переопределяет метод __str__.
    """
    name = models.CharField(max_length=256,
                            verbose_name='Название')
    slug = models.SlugField(max_length=50,
                            unique=True,
                            verbose_name='Слаг')

    class Meta:
        abstract = True
        default_permissions = (
            'add', 'delete', 'view'
        )

    def __str__(self):
        return self.name
