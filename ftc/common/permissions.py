
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser:
            return True
        if hasattr(obj, 'created_by'):
            return obj == request.user
        return False


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return False


class AnonCreate(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous and request.method == 'POST':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous and request.method == 'POST':
            return True
        return False


class IsOwnerAdminOrCreate(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        if request.method == 'POST':
            return True
        if request.user.is_superuser:
            return True
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        return False
