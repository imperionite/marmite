from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow only owners of an object or admins to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admins have full access
        if user.is_staff or user.role == "admin" or user.groups.filter(name="Admin").exists():
            return True

        # Check if the object has 'user' or 'author' and compare it with the request user
        return hasattr(obj, 'user') and obj.user == request.user or hasattr(obj, 'author') and obj.author == request.user
    
       