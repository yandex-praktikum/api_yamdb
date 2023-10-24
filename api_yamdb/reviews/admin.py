from django.contrib import admin

from .models import Category, Genre, Title

admin.site.empty_value_display = 'Не задано'


class TitleInline(admin.TabularInline):
    model = Title
    extra = 0


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
    )
    list_editable = (
        'name',
        'year',
        'description',
        'category',
    )
    list_filter = (
        'category',
        'genre',
        'name',
        'year',
    )
    list_display_links = ('id',)
    filter_horizontal = ('genre',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        TitleInline,
    )
    list_display = (
        'name',
        'slug',
    )
    list_display_links = (
        'name',
        'slug',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_display_links = (
        'name',
        'slug',
    )
