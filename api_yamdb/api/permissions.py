from rest_framework import permissions

from .constants import USER_ROLES_ADMIN_TUPLE, ADMIN_ROLE_ENG

# Должен быть доступ без токена
class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.role[USER_ROLES_ADMIN_TUPLE][ADMIN_ROLE_ENG]
                == 'admin')  # Или правильнее импортировать USER_ROLES?
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.role[USER_ROLES_ADMIN_TUPLE][ADMIN_ROLE_ENG]
                == 'admin')  # Тот же вопрос
