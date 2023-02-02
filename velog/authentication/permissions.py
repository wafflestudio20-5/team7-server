from rest_framework import permissions


class IsCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
    
from .models import User

class IsAccountOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: User):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj == request.user
