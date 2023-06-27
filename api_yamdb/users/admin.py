from django.contrib import admin

# from reviews.models import Category, Genre, Title, Review, Comment
# from users.models import User


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_display_links = ('name',)
    search_fields = (
        'name',
        'slug',
    )
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    list_editable = ('slug',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_display_links = ('name',)
    search_fields = (
        'name',
        'slug',
    )
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    list_editable = ('slug',)


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'category',
        'description',
    )
    search_fields = (
        'name',
        'year',
        'category',
        'genre',
    )
    list_filter = ('year',)
    empty_value_display = '-пусто-'
    list_editable = (
        'name',
        'year',
        'category',
        'description',
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'created',
        'rating',
    )
    search_fields = (
        'text',
        'author',
        'title',
    )
    list_filter = ('created',)
    empty_value_display = '-пусто-'
    list_editable = (
        'author',
        'title',
        'text',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'review',
        'author',
        'created',
    )
    search_fields = (
        'text',
        'author',
    )
    empty_value_display = '-пусто-'
    list_editable = (
        'author',
        'text',
    )


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )
    list_filter = (
        'first_name',
        'last_name',
        'role',
    )
    empty_value_display = '-пусто-'
    list_editable = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
    )


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Genre, GenreAdmin)
# admin.site.register(Title, TitleAdmin)
# admin.site.register(Review, ReviewAdmin)
# admin.site.register(Comment, CommentAdmin)
# admin.site.register(User, UsersAdmin)
