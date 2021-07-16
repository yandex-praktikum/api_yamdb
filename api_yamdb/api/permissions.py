from rest_framework.permissions import BasePermission, SAFE_METHODS


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
        # if (request.user.role == "User") and (request.method in ('GET',)):
        #     return True
        # if (request.user.role == "Admin") and (request.method in ('GET', 'POST', 'PATCH', 'DELETE',)):
        #      return True

        return True

# class IsMe(BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in ('PATCH',):
#                 return obj.author == request.user
#         return False

