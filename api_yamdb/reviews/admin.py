from django.contrib import admin
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title

admin.site.empty_value_display = 'Не задано'


class UserAdmin(admin.ModelAdmin):
    """Интерфейс админ-зоны пользователей."""

    list_display = ('username', 'email', 'role')
    list_editable = ('role',)
    search_fields = ('username', 'email', 'role')
    list_filter = ('role',)
    list_display_links = ('username',)


class TitleAdmin(admin.ModelAdmin):
    """Интерфейс админ-зоны произведений."""

    list_display = ('name', 'year', 'category')
    list_editable = ('category',)
    search_fields = ('category', 'genre')
    list_filter = ('category', 'genre', 'year')
    list_display_links = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    """Интерфейс админ-зоны категорий."""

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_display_links = ('name',)


class GenreAdmin(admin.ModelAdmin):
    """Интерфейс админ-зоны жанров."""

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_display_links = ('name',)


admin.site.register(get_user_model(), UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
