from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from core import constants as const
from reviews.models import Category, Genre, Title, Review, Comment, TitleGenre

User = get_user_model()


class TitleGenreInline(admin.TabularInline):
    model = TitleGenre
    extra = 1


@admin.register(User)
class YamdbUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    fieldsets += (('Extra Fields', {'fields': ('bio', 'role')}),)
    list_display = ('pk', 'username', 'email', 'role')
    list_editable = ('role',)
    list_filter = ('role',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name', 'slug')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = [TitleGenreInline]
    list_display = ('pk', 'name', 'year', 'category', 'get_genre_list')
    list_editable = ('category',)
    list_select_related = ['category',]
    search_fields = ('name',)
    list_per_page = const.OBJECTS_PER_PAGE

    def get_genre_list(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])
    get_genre_list.short_description = 'Жанры'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'score', 'text', 'pub_date')
    list_select_related = ['title', 'author']
    search_fields = ('title',)
    list_filter = ('pub_date',)
    ordering = ['-pub_date']
    list_per_page = const.OBJECTS_PER_PAGE


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'author', 'text', 'pub_date')
    list_select_related = ['review', 'author']
    search_fields = ('review',)
    list_filter = ('pub_date',)
    ordering = ['-pub_date']
    list_per_page = const.OBJECTS_PER_PAGE
