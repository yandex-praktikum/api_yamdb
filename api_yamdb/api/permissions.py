from rest_framework.permissions import SAFE_METHODS, BasePermission

from models import MODERATOR_ROLE, ADMIN_ROLE


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if (request.method not in SAFE_METHODS
                and request.user.is_anonymous):
            return False
        return (request.method in SAFE_METHODS
                or request.user.is_admin
                or request.user.is_superuser)


class IsMeAction(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.method == 'PATCH' and request.user.role == ADMIN_ROLE:
            return True
        return request.method in ('GET', 'PATCH', 'DELETE')


class IsAdminModeratorOrAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return ((request.user.role == ADMIN_ROLE
                 or request.user.role == MODERATOR_ROLE
                 or request.user.is_superuser
                 or obj.author == request.user)
                and (request.method in ('PATCH', 'DELETE',)))
