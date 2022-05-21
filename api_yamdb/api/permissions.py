from rest_framework.permissions import BasePermission
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReviewCommentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        if request.user.is_authenticated and (
            request.user.role == "admin" or request.user.role == "moderator"
        ):
            return True
        if request.method == ("PATCH" or "DELETE"):
            return obj.author == request.user


class GenreCategoryPermission(BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_admin
                )


class OwnerOrAdmins(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_admin
            or request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    """Разрешение на уровне админ."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class AuthorAndStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_moderator
                )
            )
        )
