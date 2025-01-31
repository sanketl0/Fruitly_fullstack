# permissions.py

from rest_framework import permissions


class IsUseradmin(permissions.BasePermission):
    """
    Allows access only to user1 or admin roles.
    """
    def has_permission(self, request, view):
        user_role = request.user.role
        return user_role == 'admin'

class IsUser1(permissions.BasePermission):
    """
    Allows access only to user1 or admin roles.
    """
    def has_permission(self, request, view):
        user_role = request.user.role
        return user_role == 'user1'


class IsUser2(permissions.BasePermission):
    """
    Allows access only to user2 role.
    """
    def has_permission(self, request, view):
        user_role = request.user.role
        return user_role == 'user2'


class IsUser1OrUser2(permissions.BasePermission):
    """
    Allows access if user is either user1 or user2.
    """
    def has_permission(self, request, view):
        user_role = request.user.role
        return user_role in ['user1', 'user2']