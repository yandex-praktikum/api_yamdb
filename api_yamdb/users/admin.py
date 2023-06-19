from django.contrib import admin
from users.models import User
from django.contrib.auth import get_user_model
from reviews.models import (Categories,
                            Genres,
                            Titles,
                            Reviews,
                            Comments)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    list_display_links = ('name',)
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    list_editable = ('slug',)


class GenresAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    list_display_links = ('name',)
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    list_editable = ('slug',)


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'description',)
    search_fields = ('name', 'year', 'category', 'genre',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'
    list_editable = ('name', 'year', 'category', 'description',)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'created', 'rating',)
    search_fields = ('text', 'author', 'title',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'
    list_editable = ('author', 'title', 'text',)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'review', 'author', 'created',)
    search_fields = ('text', 'author',)
    empty_value_display = '-пусто-'
    list_editable = ('author', 'text',)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'userrole',)
    search_fields = ('username', 'email', 'first_name', 'last_name',
                     'userrole',)
    list_filter = ('first_name', 'last_name', 'userrole',)
    empty_value_display = '-пусто-'
    list_editable = ('username', 'email', 'first_name', 'last_name',
                     'userrole',)
    


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(User, UsersAdmin)