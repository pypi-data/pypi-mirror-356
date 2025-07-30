PERMISSIONS = """
from rest_framework import permissions


class {model}BasePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
"""
