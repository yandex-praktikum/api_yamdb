from rest_framework.permissions import BasePermission


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
