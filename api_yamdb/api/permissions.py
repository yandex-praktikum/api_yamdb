from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.author)


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        user = request.user
        return bool(user.is_authenticated and user.role == 'admin')


class IsSafeMethod(BasePermission):

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS)


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        user = request.user.is_authenticated
        return bool(user and request.user.role == 'moderator')

    def has_object_permission(self, request, view, obj):
        user = request.user.is_authenticated
        return bool(user and request.user.role == 'moderator')


class HasUsernameForPOST(BasePermission):
    # Since the message has been rewritten, that permission should be placed
    # last and joined with "&"(AND) or ","(comma) to display the correct
    # matching answer.
    message = ('Вы не можете оставлять отзывы и комментарии без '
               'предварительной установки параметра username через '
               'PATCH-запрос на адрес api/v1/users/me/')

    def has_permission(self, request, view):
        return bool(request.method != 'POST' or request.user.username)
