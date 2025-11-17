from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow employees to access their own location records.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to only allow owners of a location to access it.
        """
        # Employees can only access their own location records
        return obj.employee == request.user
