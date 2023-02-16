from django.contrib import admin

from .models import Review, Comment


class ReviewAdmin(admin.ModelAdmin):
    """Настройка админки отзывов к произведеням."""
    list_display = ('id', 'author', 'title', 'text', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('score', 'author', 'pub_date')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    """Настройка админки комментариев к отзывам."""
    list_display = ('id', 'author', 'review', 'text', 'pub_date')
    search_fields = ('text',)
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'


admin.site.register(Review)
admin.site.register(Comment)
