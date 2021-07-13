from django.db import models

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
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(verbose_name='Рейтинг', choices=RATING_LEVELS)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.text