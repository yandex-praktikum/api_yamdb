from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class IsHasUsername(BasePermission):
    massage = ('Вы не можете оставлять отзывы и комментарии без '
               'предварительной установки параметра username через '
               'PATCH-запрос на адрес api/v1/users/me/')

    def has_object_permission(self, request, view, obj):
        return request.user.username


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        user = request.user.is_authenticated
        return user and request.user.role == 'moderator'

    def has_object_permission(self, request, view, obj):
        user = request.user.is_authenticated
        return user and request.user.role == 'moderator'
