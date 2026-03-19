"""RBAC permission classes."""
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Only admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsContentManager(BasePermission):
    """Content managers or admins."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ('content_manager', 'admin')
        )


class IsVerified(BasePermission):
    """Only email-verified users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_verified
