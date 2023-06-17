from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrAdminsOrReadOnly(BasePermission):
    """Разрешения для роли хозяина"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (obj == request.user or request.user.is_admin
                or request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    """Разрешение для роли админ."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAuthorOrStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_moderator
                )
            )
        )    