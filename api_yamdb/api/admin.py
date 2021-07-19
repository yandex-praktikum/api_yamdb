from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, Genre, Review, Title, User

EMPTY_VALUE = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year')
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'pub_date',
        'text', 'title', 'score'
    )
    search_fields = ('author',)
    empty_value_display = EMPTY_VALUE


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'pub_date',
        'review', 'text'
    )
    search_fields = ('author',)
    empty_value_display = EMPTY_VALUE


admin.site.register(User, UserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
