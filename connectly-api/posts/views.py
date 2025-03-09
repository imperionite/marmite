from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import logging

from .models import Post, Comment, Like, Follow
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LoginSerializer, FeedPostSerializer, FollowSerializer
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
    def comment(self, request, pk=None):
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
    
# View for Validating JWT
class ValidateTokenView(APIView):
    def post(self, request, *args, **kwargs):
        jwt_auth = JWTAuthentication()
        
        # Extract token from request headers or body as needed
        token = request.data.get('token')  # Assuming token is sent in the body
        
        try:
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            return Response({
                'status': True,
                'message': 'Token is valid',
                'user_id': user.id,
                'username': user.username,
            })
        except TokenError as e:
            return Response({
                'status': False,
                'message': str(e),
            }, status=401)
    
class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        # Get the refresh token from the request data
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=400)

        try:
            # Validate and decode the provided refresh token
            refresh = RefreshToken(refresh_token)

            # If the refresh token is valid, generate new access and refresh tokens for the user
            new_access_token = refresh.access_token
            new_refresh_token = RefreshToken.for_user(refresh.user)  # New refresh token for the user

            # Return both the new access token and refresh token
            return Response({
                'access': str(new_access_token),
                'refresh': str(new_refresh_token)  # Optional: Include new refresh token
            })

        except Exception as e:
            # If the refresh token is invalid, return an error
            return Response({"detail": "Invalid refresh token."}, status=400)
        

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1:5173/" # frontend url

    def post(self, request, *args, **kwargs):
        # Call the parent class's post method to handle the OAuth process
        response = super().post(request, *args, **kwargs)
        
        # If the response is successful, generate and return JWT tokens
        if response.status_code == 200:
            user = self.user  # The user object associated with this login
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)  # Access token
            refresh_token = str(refresh)  # Refresh token

            # Return the tokens in the response
            return Response({
                'access': access_token,
                'refresh': refresh_token
            }, status=status.HTTP_200_OK)
        else:
            # If there was an error, return the response from the parent class
            return response
        

class FeedPagination(PageNumberPagination):
    """
    Pagination class for the feed view.
    Sets the default page size and allows customization via query parameters.
    """
    page_size = 10  # Default number of posts per page
    page_size_query_param = 'page_size'  # Query parameter to change page size
    max_page_size = 100  # Maximum allowed page size

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed_view(request):
    """
    Retrieves a paginated list of posts, with optional filtering by followed users or liked posts.

    Query Parameters:
    - filter (optional): 'followed' or 'liked' to filter posts.

    Returns:
    - Paginated list of posts, serialized using FeedPostSerializer.
    """
    user = request.user  # Get the authenticated user
    filter_type = request.query_params.get('filter', None)  # Get the filter type from query parameters

    if filter_type == 'followed':
        # Filter posts from users followed by the current user
        followed_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
        posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
    elif filter_type == 'liked':
        # Filter posts liked by the current user
        liked_posts = Like.objects.filter(user=user).values_list('post', flat=True)
        posts = Post.objects.filter(id__in=liked_posts).order_by('-created_at')
    else:
        # Return all posts if no filter is specified
        posts = Post.objects.all().order_by('-created_at')

    paginator = FeedPagination()  # Initialize pagination
    result_page = paginator.paginate_queryset(posts, request)  # Paginate the queryset
    serializer = FeedPostSerializer(result_page, many=True)  # Serialize the paginated results
    return paginator.get_paginated_response(serializer.data)  # Return the paginated response


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    def get_queryset(self):
        # Allow users to only see their own follow relationships
        return Follow.objects.filter(follower=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.follower == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You do not have permission to delete this follow relationship."}, status=status.HTTP_403_FORBIDDEN)