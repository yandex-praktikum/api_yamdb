from rest_framework import permissions

from .models import User


class IsAdminOrReadOnlyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return  request.method in permissions.SAFE_METHODS \
            or (request.user.is_superuser \
            or request.user.role == User.ADMIN)

    def has_object_permission(self, request, view, obj):
        return  request.method in permissions.SAFE_METHODS \
            or (request.user.is_superuser \
            or request.user.role == User.ADMIN)


class IsStaffOrReadOnlyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
        ) or request.user.role == User.MODERATOR \
            or request.user.role == User.ADMIN

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
        ) or request.user.role == User.MODERATOR \
            or request.user.role == User.ADMIN


class IsOwnerOrReadOnlyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ('POST', 'PUT', 'GET', 'PATCH', 'DELETE'):
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.method in ('POST', 'PUT', 'GET'):
            return True
        if request.method in ('PATCH', 'DELETE'):
            return request.user == obj.author \
                or request.user.role == User.MODERATOR \
                or request.user.role == User.ADMIN
        return False
