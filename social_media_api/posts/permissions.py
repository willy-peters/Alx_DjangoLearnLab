from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission: allow read for any, but write only for owner.
    """

    def has_object_permission(self, request, view, obj):
        # read permissions for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        # assume model instances have `author` attribute
        return getattr(obj, 'author', None) == request.user

