from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Post
from .serializers import UserSerializer, PostSerializer

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

