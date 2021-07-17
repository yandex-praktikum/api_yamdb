from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class APIUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'bio', 'is_staff', 'is_superuser')
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'is_staff', 'is_superuser')}),
    )
    ordering = ('id',)


admin.site.register(User, APIUserAdmin)
