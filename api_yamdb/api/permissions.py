from rest_framework.permissions import SAFE_METHODS, BasePermission


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
        return request.method in ('GET', 'PATCH', 'DELETE')


class IsAdminModeratorOrAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return ((request.user.role == 'admin'
                 or request.user.role == 'moderator'
                 or request.user.is_superuser
                 or obj.author == request.user)
                and (request.method in ('PATCH', 'DELETE',)))
