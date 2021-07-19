from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Reviews, Comments


class APIUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'bio', 'is_staff', 'is_superuser')
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'is_staff', 'is_superuser')}),
    )
    ordering = ('id',)


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '--пусто--'


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)


admin.site.register(User, APIUserAdmin)
