from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()

class IsPostAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow only owners of an object or admins to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user.is_staff:
            return True

        # Owners can view, update, or delete their own objects
        return obj == request.user  # Ensure obj is the user instance

class IsCommentAuthor(BasePermission):
    """
    Custom permission to allow only the author of a comment to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the author of the comment
        return obj.user == request.user