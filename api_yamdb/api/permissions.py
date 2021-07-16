from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser


class IsAdminOrDenied(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return True

