from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings 
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import logging
from django.core.cache import cache
from .models import Post, Comment, Like, Follow
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LoginSerializer, FeedPostSerializer, FollowSerializer
from .permissions import IsOwnerOrAdmin

User = get_user_model()
logger = logging.getLogger(__name__)

FEED_CACHE_TIMEOUT = getattr(settings, 'FEED_CACHE_TIMEOUT', 7200)

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
        cache.delete(f'user_{self.get_object().id}')
        cache.delete('feed_view') 
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()

        response_data = {
            'id': user.id,
            'username': user.username,
            'message': 'User created successfully'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        cache_key = f'user_{instance.id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        else:
            data = serializer.data
            cache.set(cache_key, data, settings.CACHE_TTL)
            return Response(data)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user or request.user.is_staff or request.user.role == "admin" or request.user.groups.filter(name="Admin").exists():
            self.perform_destroy(user)
            cache.delete(f'user_{self.get_object().id}')
            cache.delete('feed_view') 
            return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You do not have permission to delete this account.'}, status=status.HTTP_403_FORBIDDEN)

class CommentPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Post objects.
    Includes additional actions for liking, unliking, and commenting on posts.
    Only post owners or admin users can update or delete a post.
    Privacy settings and RBAC enforced.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        Enforces privacy settings and filters posts accordingly.
        """
        user = self.request.user
        if user.is_authenticated:
            # Admin can see all private posts
            if user.is_staff or user.role == "admin" or user.groups.filter(name="Admin").exists():
                return Post.objects.all()  # Admin can see everything
                # Owner can see all their private posts, plus public posts and those from followers
            return Post.objects.filter(
                Q(privacy='public') |
                Q(author=user) |
                Q(author__followers__follower=user)
            ).distinct()
        return Post.objects.filter(privacy='public')  # Public posts visible to everyone

    def get_permissions(self):
        """
        Returns the appropriate permissions based on the action.
        """
        if self.action in ['list', 'retrieve', 'comments', 'likes']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['create', 'like', 'unlike', 'comment']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        self.clear_feed_cache(self.request.user.id) # Clear feed cache on post creation

    def perform_update(self, serializer):
        serializer.save()
        self.clear_feed_cache(serializer.instance.author.id) # Clear feed cache on post update

    def perform_destroy(self, instance):
        author_id = instance.author.id
        instance.delete()
        self.clear_feed_cache(author_id) # Clear feed cache on post deletion

    def clear_feed_cache(self, user_id):
        """Helper function to clear feed cache for a specific user."""
        keys_to_delete = cache.keys(f'feed_data:{user_id}:*')
        if keys_to_delete:
            cache.delete_many(keys_to_delete, cache=cache.caches['feed_cache'])
            logger.info(f"Cleared feed cache for user: {user_id}")

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Retrieves all comments for a specific post with pagination and caching.
        """
        post = self.get_object()
        page = request.query_params.get('page')
        cache_key = f'post_comments:{post.pk}:{page}'
        cached_comments = cache.get(cache_key)

        if cached_comments:
            logger.info(f"Cache hit for key: {cache_key}")
            return Response(cached_comments)
        else:
            logger.info(f"Cache miss for key: {cache_key}")
            paginator = CommentPagination()
            result_page = paginator.paginate_queryset(post.comments.all(), request)
            serializer = CommentSerializer(result_page, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            cache.set(cache_key, response_data.data, timeout=3600) # Cache for 1 hour
            return response_data

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if Like.objects.filter(user=user, post=post).exists():
            return Response({'message': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
        Like.objects.create(user=user, post=post)
        self.clear_feed_cache_for_followers(post.author.id) # Clear feed cache for followers
        return Response({'message': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like = Like.objects.filter(user=user, post=post)
        if not like.exists():
            return Response({'message': 'You have not liked this post yet.'}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        self.clear_feed_cache_for_followers(post.author.id) # Clear feed cache for followers
        return Response({'message': 'Post unliked successfully.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, post=post)
            self.clear_post_comments_cache(post.pk) # Clear comments cache
            self.clear_feed_cache_for_followers(post.author.id) # Clear feed cache for followers
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def clear_post_comments_cache(self, post_id):
        """Helper function to clear comments cache for a specific post."""
        keys_to_delete = cache.keys(f'post_comments:{post_id}:*')
        if keys_to_delete:
            cache.delete_many(keys_to_delete)
            logger.info(f"Cleared comments cache for post: {post_id}")

    def clear_feed_cache_for_followers(self, author_id):
        """Helper function to clear feed caches of users following the post author."""
        followers = Follow.objects.filter(following=author_id).values_list('follower_id', flat=True)
        for follower_id in followers:
            self.clear_feed_cache(follower_id)

class CommentViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for comments with RBAC enforcement.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Clear post comments cache and feed cache of the post author's followers
        post_id = serializer.instance.post_id
        post = Post.objects.get(pk=post_id)
        PostViewSet().clear_post_comments_cache(post_id)
        PostViewSet().clear_feed_cache_for_followers(post.author.id)

    def perform_update(self, serializer):
        serializer.save()
        # Clear post comments cache and feed cache of the post author's followers
        post_id = serializer.instance.post_id
        post = Post.objects.get(pk=post_id)
        PostViewSet().clear_post_comments_cache(post_id)
        PostViewSet().clear_feed_cache_for_followers(post.author.id)

    def perform_destroy(self, instance):
        post_id = instance.post_id
        post = Post.objects.get(pk=post_id)
        PostViewSet().clear_post_comments_cache(post_id)
        PostViewSet().clear_feed_cache_for_followers(post.author.id)
        instance.delete()


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        if post.privacy == 'private' and post.author != request.user:
            return Response({'message': 'This post is private.'}, status=status.HTTP_403_FORBIDDEN)
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
    
class ValidateTokenView(APIView):
    def post(self, request, *args, **kwargs):
        jwt_auth = JWTAuthentication()
        token = request.data.get('token')
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
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=400)
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = refresh.access_token
            new_refresh_token = RefreshToken.for_user(refresh.user)
            return Response({
                'access': str(new_access_token),
                'refresh': str(new_refresh_token)
            })
        except Exception as e:
            return Response({"detail": "Invalid refresh token."}, status=400)

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1:5173/"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = self.user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                'access': access_token,
                'refresh': refresh_token
            }, status=status.HTTP_200_OK)
        else:
            return response

class FeedPagination(PageNumberPagination):
    page_size = 10  # Adjust as needed
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed_view(request):
    user = request.user
    filter_type = request.query_params.get('filter', None)
    page = request.query_params.get('page')

    cache_key = f'feed_data:{user.id}:{filter_type}:{page}'
    cached_feed = cache.get(cache_key)

    if cached_feed:
        logger.info(f"Cache hit for key: {cache_key}")
        return Response(cached_feed)
    else:
        logger.info(f"Cache miss for key: {cache_key}")
        try:
            if filter_type == 'followed':
                followed_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
                posts = Post.objects.filter(author__in=followed_users)
            elif filter_type == 'liked':
                liked_posts = Like.objects.filter(user=user).values_list('post', flat=True)
                posts = Post.objects.filter(id__in=liked_posts)
            else:
                # posts = Post.objects.select_related('author').prefetch_related('likes', 'comments').all()
                posts = Post.objects.select_related('author').only('id', 'author_id', 'content', 'privacy')


            posts = posts.filter(
                Q(privacy='public') |
                Q(author=user) |
                Q(author__followers__follower=user)
            ).distinct().order_by('-created_at')

            paginator = FeedPagination()
            paginated_posts = paginator.paginate_queryset(posts, request)
            serializer = FeedPostSerializer(paginated_posts, many=True)
            response_data = paginator.get_paginated_response(serializer.data)
            cache_timeout = FEED_CACHE_TIMEOUT  # Use the configurable timeout
            cache.set(cache_key, response_data.data, timeout=cache_timeout)
            return response_data
        except Exception as e:
            logger.error(f"Error in feed_view: {e}", exc_info=True)
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        cache.delete(f'user_{request.user.id}_follows')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.follower == request.user:
            self.perform_destroy(instance)
            cache.delete(f'user_{request.user.id}_follows')
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You do not have permission to delete this follow relationship."}, status=status.HTTP_403_FORBIDDEN)