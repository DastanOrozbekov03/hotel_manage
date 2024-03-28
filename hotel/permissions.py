from rest_framework import permissions

class IsOwnerOrSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_superuser

class ReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access.
    """

    def has_permission(self, request, view):
        """
        Check if the request method is safe (GET, HEAD, OPTIONS).
        """
        return request.method in permissions.SAFE_METHODS