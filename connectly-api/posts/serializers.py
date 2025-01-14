from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at']
