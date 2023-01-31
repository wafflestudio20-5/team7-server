from rest_framework import permissions

from .models import Post


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        if request.method in ('GET', 'POST', 'HEAD', 'OPTIONS'):
            return True
        else:
            return obj.author == request.user

class IsCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        return obj.author ==request.user

