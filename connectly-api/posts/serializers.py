from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from validate_email import validate_email
from .models import Post, Comment, Like, Follow

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True) # Added role field

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'created_at', 'role'] # Added role field
    
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
        fields = ['id', 'content', 'created_at', 'user', 'post']
        read_only_fields = ['user', 'post']

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
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'comments', 'privacy']
        read_only_fields = ['id', 'author', 'created_at']
    
    def validate_content(self, value):
        if len(value) < 7:
            raise serializers.ValidationError("Post content must be at least 7 characters long.")
        return value

    def validate_author(self, value):
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Author not found.")
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom fields to the token payload
        data['username'] = self.user.username
        data['email'] = self.user.email

        return data
    

class LoginSerializer(serializers.Serializer):
    """
    Instead of manually handling tokens, it is recommended to use DRF SimpleJWT's built-in token handling for better security and maintainability.
    This rserializer authenticates users using the provided identifier and password, then generates JWT tokens using RefreshToken from SimpleJWT.
    """
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=identifier, password=password)
        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.')

        # Generate JWT token using the custom serializer
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Use the custom serializer to add username and email to the payload
        serializer = CustomTokenObtainPairSerializer()
        token = serializer.get_token(user)
        token['access'] = access_token
        return {
            'refresh': str(refresh),
            'access': access_token,
        }
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]
        read_only_fields = ["user"]

class FeedPostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    privacy = serializers.CharField(read_only=True) #added privacy

    class Meta:
        model = Post
        fields = ['id', 'content', 'author_username', 'created_at', 'like_count', 'comment_count', 'privacy'] #added privacy

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['follower', 'created_at']