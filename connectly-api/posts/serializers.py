from rest_framework import serializers
from django.contrib.auth import get_user_model
from validate_email import validate_email

from .models import Post, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at']
    
    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        return value
    
    def validate_email(self, value):
        if not validate_email(value):
            raise serializers.ValidationError("Invalid email address")
        return value

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']

    def validate_post(self, value):
        if not Post.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Post not found")
        return value

    def validate_author(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Author not found")
        return value

    def validate_text(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Comment text must be at least 5 characters long")
        return value

class PostSerializer(serializers.ModelSerializer):
    # The comments field in the serializer is used to represent the reverse relationship from the Post model to the Comment model. 
    # This relationship is established through the related_name='comments' argument in the post field of the Comment model.
    # For consistency, readability and flexibility, nested serializer was used.
    
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'comments']
    
    def validate_content(self, value):
        if len(value) < 7:
            raise serializers.ValidationError("Post content must be at least 7 characters long.")
        return value

    def validate_author(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Author not found.")
        return value

