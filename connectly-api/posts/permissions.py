from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow only owners of an object or admins to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user.is_staff:
            return True

        # Check if the object has 'user' or 'author' and compare it with the request user
        return hasattr(obj, 'user') and obj.user == request.user or hasattr(obj, 'author') and obj.author == request.user
    
       