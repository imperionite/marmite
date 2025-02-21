from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# from djoser.serializers import UserSerializer
from validate_email import validate_email # type: ignore

from .models import Post, Comment, Like

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at'] # Exclude sensitive fields like password
    
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
        fields = '__all__'

    def validate_post(self, value):
        if not Post.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Post not found")
        return value

    def validate_user(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Author not found")
        return value

    def validate_content(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Comment text must be at least 5 characters long")
        return value

class PostSerializer(serializers.ModelSerializer):
    
    """
    The comments field in the serializer is used to represent the reverse relationship from the Post model to the Comment model. 
    This relationship is established through the related_name='comments' argument in the post field of the Comment model.
    For consistency, readability and flexibility, nested serializer was used.
    """
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'comments',]
        read_only_fields = ['id', 'author', 'created_at',] 
    
    def validate_content(self, value):
        if len(value) < 7:
            raise serializers.ValidationError("Post content must be at least 7 characters long.")
        return value

    def validate_author(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Author not found.")
        return value


class LoginSerializer(serializers.Serializer):
    """
    Instead of manually handling tokens, it is recommended to use DRF SimpleJWT's built-in token handling for better security and maintainability.
    This revised serializer authenticates users using the provided identifier and password, then generates JWT tokens using RefreshToken from SimpleJWT.
    """
    identifier = serializers.CharField()  # Can be email or username
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        # Authenticate user using custom backend
        user = authenticate(request=self.context.get('request'), username=identifier, password=password)
        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.')

       # Generate JWT token for authenticated user
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for the Like model"""

    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]
        read_only_fields = ["user"]  # Ensure user is set automatically