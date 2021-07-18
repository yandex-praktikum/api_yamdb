from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.author)


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and user.role == 'admin')


class IsSafeMethod(BasePermission):

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)


class HasUsernameForPOST(BasePermission):
    message = ('Вы не можете оставлять отзывы и комментарии без '
               'предварительной установки параметра username через '
               'PATCH-запрос на адрес api/v1/users/me/')

    def has_permission(self, request, view):
        return bool(request.method != 'POST' or request.user.username)


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        user = request.user.is_authenticated
        return bool(user and request.user.role == 'moderator')
