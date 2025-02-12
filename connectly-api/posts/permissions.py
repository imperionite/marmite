from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from .models import Post, Like

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()

class IsPostAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

class CanLikePost(BasePermission):
    """ Custom permission to allow liking a post only once """
    def has_permission(self, request, view):
        post_id = view.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        return not Like.objects.filter(user=request.user, post=post).exists()  # Deny if already liked