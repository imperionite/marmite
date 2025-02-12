from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LoginSerializer, LikeSerializer
from .permissions import IsAdmin, IsPostAuthor, CanLikePost

User = get_user_model()

from rest_framework import status
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Set password after saving to hash it properly
        user.set_password(request.data['password'])
       
        user.save()
        # Get the newly created user instance
        userInstance = serializer.instance
        response_data = {
            'id': userInstance.id,
            'message': 'User created successfully'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Get the newly created post instance
        postInstance = serializer.instance

        # Customize the response data
        response_data = {
            'id': postInstance.id,
            'message': 'Post created successfully',
        }

        # Return the custom response
        return Response(response_data, status=status.HTTP_201_CREATED)
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Get the newly created comment instance
        commentInstance = serializer.instance

        # Customize the response data
        response_data = {
            'text': commentInstance.text,
            'author': commentInstance.author.id,
            'post': commentInstance.post.id,
        }

        # Return the custom response
        return Response(response_data, status=status.HTTP_201_CREATED)
    

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
    
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        self.check_object_permissions(request, post)
        return Response({"content": post.content})

class AdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "Hello, Admin!"})
    
class ProtectedView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        content = {'message': 'This is a protected route, accessible only to authenticated users.'}

        return Response(content)
    

class LikeViewSet(viewsets.ModelViewSet):
    """
    Handles liking and unliking posts.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, CanLikePost]

    def create(self, request, *args, **kwargs):
        """
        Handles the like action.
        """
        post = get_object_or_404(Post, id=request.data.get('post'))
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Handles the unlike action.
        """
        like = get_object_or_404(Like, id=kwargs['pk'], user=request.user)
        like.delete()
        return Response({"message": "Post unliked successfully."}, status=status.HTTP_204_NO_CONTENT)


