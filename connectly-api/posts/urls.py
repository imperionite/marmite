from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import UserViewSet, PostViewSet, CommentViewSet, LoginView, ProtectedView, PostDetailView, AdminView, LikeViewSet
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
router.register(r'likes', LikeViewSet, basename='like')

urlpatterns = [
    path('protected/', ProtectedView.as_view(), name='protected'), # sanity check
    path('users/login/', LoginView.as_view(), name='login'),
    path('<int:pk>/', PostDetailView.as_view()),
    path('admin/', AdminView.as_view()),
] + router.urls