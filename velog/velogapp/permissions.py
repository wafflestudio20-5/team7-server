from rest_framework import permissions

from .models import Post


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.created_by == request.user


class IsCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        return obj.created_by == request.user
