from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import UserViewSet, PostViewSet, CommentViewSet, LoginView, ProtectedView, PostDetailView, AdminView, feed_view, FollowViewSet
from django.conf import settings

# Choose router based on DEBUG setting
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# Register viewsets with the router
router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'follows', FollowViewSet, basename='follow')

# Add the login endpoint
urlpatterns = [
    path('users/login/', LoginView.as_view(), name='login'),
    path('<int:pk>/', PostDetailView.as_view()),
    path('protected/', ProtectedView.as_view(), name='protected'), # sanity check
    path('admin/', AdminView.as_view()),
    path('feed/', feed_view, name='feed'),
] + router.urls