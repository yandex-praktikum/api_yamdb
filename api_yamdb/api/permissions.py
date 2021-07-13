from rest_framework import permissions

from api.models import User


class IsAuthorOrStuffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return not request.user.is_anonymous()
        if request.method in ('PATCH', 'DELETE'):
            return (obj.author == request.user
                    or request.user.role == User.role.user
                    or request.user.role == User.role.moderator)
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
