from django.contrib import admin
from .models import Category, Genre, Title
from import_export.admin import ImportMixin
from .resources import CategoryResource, GenreResource, TitleResource

class CategoryAdmin(ImportMixin,admin.ModelAdmin):

    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'
    resource_class = CategoryResource


admin.site.register(Category, CategoryAdmin)


class GenreAdmin(ImportMixin,admin.ModelAdmin):

    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'
    resource_class = GenreResource


admin.site.register(Genre, GenreAdmin)


class TitleAdmin(ImportMixin,admin.ModelAdmin):

    list_display = ('pk', 'name', 'year', 'category', 'description',)
    search_fields = ('description',)
    empty_value_display = '-пусто-'
    resource_class = TitleResource


admin.site.register(Title, TitleAdmin)