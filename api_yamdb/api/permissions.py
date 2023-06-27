from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticatedOrReadOnly)


class IsAdminOnly(BasePermission):
    """Разрешения для админов и суперюзеров"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class GuestReadOnly(BasePermission):
    """Разрешает только безопасные запросы."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and (
                request.user.is_superuser or request.user.is_admin))


class IsAdminModerOwnerOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_superuser
                 or request.user.is_moderator
                 or request.user == obj.author))
