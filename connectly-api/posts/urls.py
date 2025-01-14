from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import UserViewSet, PostViewSet
from django.conf import settings

# Choose router based on DEBUG setting
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# Register viewsets with the router
router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    # Custom paths for creating users and posts with /create/
    path('users/create/', UserViewSet.as_view({'post': 'create'}), name='user-create'),
    path('posts/create/', PostViewSet.as_view({'post': 'create'}), name='post-create'),
]

# Include the router URLs
urlpatterns += router.urls
