from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import UserViewSet, PostViewSet, CommentViewSet
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


# Include the router URLs
urlpatterns = router.urls
