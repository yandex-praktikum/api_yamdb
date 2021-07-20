from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Categories, Comments, Genres, Reviews, Titles, User


class APIUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'role', 'first_name',
                    'last_name', 'bio', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'username')
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'role', 'is_staff', 'is_superuser')}),
    )
    ordering = ('id',)


class ReviewsAdmin(admin.ModelAdmin):

    list_display = ('title', 'score', 'text', 'author', 'pub_date')
    list_display_links = ('text',)
    readonly_fields = ('author', )
    list_filter = ('pub_date',)
    search_fields = ('text',)
    ordering = ('-pub_date',)
    empty_value_display = '--нет--'


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    list_display_links = ('text',)
    readonly_fields = ('author',)
    list_filter = ('pub_date',)
    search_fields = ('text',)
    ordering = ('-pub_date',)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class GenresAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class TitlesAdmin(admin.ModelAdmin):

    list_display = ('name', 'year', 'description', 'category')
    list_display_links = ('name',)
    list_filter = ('category', 'genre')
    search_fields = ('name',)
    ordering = ('name',)
    empty_value_display = '--нет--'


admin.site.register(User, APIUserAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Titles, TitlesAdmin)
