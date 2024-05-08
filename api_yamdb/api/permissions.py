from rest_framework import permissions

from core import constants as const

class AuthorOrReadOnly(permissions.BasePermission):
    """Разрешения на редактирование и удаление для автора."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class UserSelfAccess(permissions.BasePermission):
    """Разрешения для владельца профиля.

    Просмотр и изменение данных профиля."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class AdminAccess(permissions.BasePermission):
    """Разрешения для администратора и суперпользователя."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))


class ModeratorAccess(permissions.BasePermission):
    """Разрешения для модератора и суперпользователя."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'moderator'
                     or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.role == 'moderator'
                     or request.user.is_superuser))


class AuthorOrModeratorOrAdminAccess(permissions.BasePermission):
    """Разрешения для модератора и суперпользователя."""

    def has_permission(self, request, view):
        return ((request.user.is_authenticated)
                or (request.method in permissions.SAFE_METHODS))

    def has_object_permission(self, request, view, obj):
        return ((request.user.is_authenticated
                and (request.user.role == 'moderator'
                     or request.user.role == 'admin'
                     or request.user.is_superuser
                     or request.user == obj.author))
                or request.method in permissions.SAFE_METHODS)


class AdminOrReadOnlyAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not (request.user.is_authenticated):
            return False
        return (request.user.role == const.ADMIN or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.role == const.ADMIN
                or request.user.is_superuser))  
