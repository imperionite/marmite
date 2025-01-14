from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        # Try to authenticate with username
        try:
            user = UserModel.objects.get(username=username)
        except ObjectDoesNotExist:
            # If username fails, try to authenticate with email
            try:
                user = UserModel.objects.get(email=username)
            except ObjectDoesNotExist:
                return None
        
        # Check password
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None