from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(permissions.BasePermission):

    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
                )


class IsModerator(BasePermission):
    """ Права модератора """

    def has_permission(self, request, view):
        return bool(request.user.is_moderator)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_moderator)


class IsAdmin(BasePermission):
    """ Права админа """

    def has_permission(self, request, view):
        return bool(request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_admin)


class IsAuthor(BasePermission):
    """ Права автора """

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.author)
