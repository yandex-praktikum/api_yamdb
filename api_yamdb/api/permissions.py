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
        if (request.get_full_path() == '/api/v1/users/me/'
                and request.method in ('DELETE')):
            return True
        if view.action == 'me' and request.method in ('GET', 'PATCH'):
            return True
        if (request.user.role == "admin" or request.user.is_superuser) and (
                request.method in ('GET', 'POST', 'PATCH', 'DELETE')
        ):
            return True
        return False


class IsAdminOrModeratororAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in ('PATCH', 'DELETE'):
            return True

        return ((request.user.role == "admin"
                or request.user.role == "moderator"
                or request.user.is_superuser
                or obj.author == request.user)
                and (request.method in ('PATCH', 'DELETE',)))
