from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrStaff(BasePermission):
    """Разрешение для автора и сотрудников
    (сурерюзеры, админы и модераторы) к объекту класса.
    Использовать для вьюшек Reviews и Comments"""
    # def has_permission(self, request, view):
    #     return (request.method in SAFE_METHODS
    #             or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and (obj.author == request.user
                     or request.user.is_superuser
                     or request.user.is_admin
                     or request.user.is_moderator))


class IsAdminOnly(BasePermission):
    """Разрешения для админов и суперюзеров"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_superuser))

    # def has_object_permission(self, request, view, obj):
    #     return (request.user.is_authenticated
    #             and (request.user.is_admin
    #                  or request.user.is_superuser))


class GuestReadOnly(BasePermission):
    """Разрешает только безопасные запросы."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

# class IsStaffOrReadOnly(BasePermission):
#     """Разрешения для сотрудников
#     (сурерюзеры, админы и модераторы)"""
#     def has_permission(self, request, view):
#         return (request.method in SAFE_METHODS
#                 or request.user.is_authenticated)

#     def has_object_permission(self, request, view, obj):
#         return (request.method in SAFE_METHODS
#                 or (request.user.is_authenticated
#                     and (request.user.is_superuser
#                          or request.user.is_admin
#                          or request.user.is_moderator)))
# class IsAuthorOrAdmins(BasePermission):
#     """Разрешене для админов и пользователей
#      для изменения данных о пользователе"""
#     def has_permission(self, request, view):
#         return request.user.is_authenticated

#     def has_object_permission(self, request, view, obj):
#         return (request.user.is_authenticated
#                 and (obj == request.user
#                      or request.user.is_superuser
#                      or request.user.is_admin))
