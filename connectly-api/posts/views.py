from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# from rest_framework.authtoken.models import Token
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
import logging

from .models import Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LoginSerializer
from .permissions import IsOwnerOrAdmin

User = get_user_model()
logger = logging.getLogger(__name__)

from rest_framework import status
from rest_framework.response import Response
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        elif self.action == 'list':
            return [IsAuthenticated()]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'password' in request.data:
            user.set_password(request.data['password'])
            user.save()

        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()

        response_data = {
            'id': user.id,
            'message': 'User created successfully'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        logger.debug(f"Request user: {request.user}, is_staff: {request.user.is_staff}, Target user: {user}")
        if request.user.is_staff or user == request.user:
            self.perform_destroy(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You do not have permission to delete this account.'}, status=status.HTTP_403_FORBIDDEN)



# Pagination for Comments
class CommentPagination(PageNumberPagination):
    page_size = 5  # Default number of comments per page
    page_size_query_param = 'page_size'
    max_page_size = 20


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Post objects.
    Includes additional actions for liking, unliking, and commenting on posts.
    Only post owners or admin users can update or delete a post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        """
        Returns the appropriate permissions based on the action.
        """
        if self.action in ['list', 'retrieve', 'comments', 'likes']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['create', 'like', 'unlike', 'add_comment']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Creates a new post.

        Automatically sets the current user as the author.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Post created successfully", "post": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        """
        Saves the post instance with the current user as the author.
        """
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a single post.

        Includes like and comment counts in the response.
        """
        post = self.get_object()
        data = self.get_serializer(post).data
        data['like_count'] = post.likes.count()
        data['comment_count'] = post.comments.count()
        return Response(data)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Retrieves all comments for a specific post with pagination.
        """
        post = self.get_object()
        paginator = CommentPagination()
        result_page = paginator.paginate_queryset(post.comments.all(), request)
        serializer = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        """
        Allows an authenticated user to like a post.

        Prevents duplicate likes from the same user.
        """
        post = self.get_object()
        user = request.user

        if Like.objects.filter(user=user, post=post).exists():
            return Response({'message': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(user=user, post=post)
        return Response({'message': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        """
        Allows an authenticated user to unlike a post.
        """
        post = self.get_object()
        user = request.user

        like = Like.objects.filter(user=user, post=post)
        if not like.exists():
            return Response({'message': 'You have not liked this post yet.'}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({'message': 'Post unliked successfully.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        """
        Allows an authenticated user to add a comment to a post.
        """
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    

class CommentViewSet(viewsets.ModelViewSet):

    """
    ViewSet for managing comments on posts.

    Allows creating, retrieving, updating, and deleting comments.
    Only the comment's author or an admin user can update or delete a comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        """
        Returns permissions based on the action.
        """
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def create(self, request, *args, **kwargs):
        """
        Creates a comment. Supports:
        - POST /comments/ with { "post": post_id, "content": "..." }
        - POST /posts/{post_id}/comments/ without needing post_id in the body
        """
        post_id = kwargs.get('post_id') or request.data.get('post')
        if not post_id:
            return Response({'error': 'Post ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        post = get_object_or_404(Post, pk=post_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, post=post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Updates a comment. Only the author or admin can update.
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates a comment.
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a comment.
        """
        return super().destroy(request, *args, **kwargs)


    
# LoginView using SimpleJWT
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        self.check_object_permissions(request, post)
        return Response({"content": post.content})

class AdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({"message": "Hello, Admin!"})
    
class ProtectedView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        content = {'message': 'This is a protected route, accessible only to authenticated users.'}

        return Response(content)

