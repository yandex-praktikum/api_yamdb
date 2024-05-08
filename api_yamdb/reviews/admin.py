from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class YamdbUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets
    fieldsets += (('Extra Fields', {'fields': ('bio', 'role')}),)
    list_display = ('pk', 'username', 'email', 'role')
    list_editable = ('role',)
    list_filter = ('role',)
