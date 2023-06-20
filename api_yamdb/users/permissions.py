from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrStaffOrReadOnly(BasePermission):
    """Разрешение для автора и сотрудников
    (сурерюзеры, админы и модераторы)"""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)


class IsStaffOrReadOnly(BasePermission):
    """Разрешения для сотрудников
    (сурерюзеры, админы и модераторы)"""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator)


class IsAdminOrReadOnly(BasePermission):
    """Разрешения для админов и суперюзеров"""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_superuser or request.user.is_admin)


class IsAuthorOrAdmins(BasePermission):
    """Разрешене для админов и пользователей
     для изменения данных о пользователе"""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.user.is_superuser
                or request.user.is_admin)
