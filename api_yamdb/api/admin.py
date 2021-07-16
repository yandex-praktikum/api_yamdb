from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Genres, Categories, Titles, Review, Comment


class GenresAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class TitlesAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year")
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "pub_date",
                    "text", "title", "score")
    search_fields = ("author",)
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "pub_date",
                    "review", "text")
    search_fields = ("author",)
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
