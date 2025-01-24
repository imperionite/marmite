from django.contrib.auth.models import UserManager
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

UserModel = get_user_model()

class CustomUserManager(UserManager):
  def get_by_natural_key(self, username):
    return self.get(
        Q(username=username) | Q(email=username)
    )

class EmailOrUsernameModelBackend(ModelBackend):
  """
  Custom backend to authenticate using either username or email
  """
  def authenticate(self, request, username=None, password=None, **kwargs):
    try:
      user = UserModel.objects.get(Q(username=username) | Q(email=username))
      if user.check_password(password):
        return user
    except ObjectDoesNotExist:
      return None

    return None

  def get_user(self, user_id):
    try:
      return UserModel.objects.get(pk=user_id)
    except ObjectDoesNotExist:
      return None