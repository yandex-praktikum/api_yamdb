from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """Разрешения на редактирование и удаление для автора."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class UserSelfAccess(permissions.BasePermission):
    """Разрешения для владельца профиля.

    Просмотр и изменение данных профиля."""

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
