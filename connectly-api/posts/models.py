from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Extending AbstractUser model for customization and flexibility
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, unique=True)
    created_at = models.DateTimeField(verbose_name='date joined', auto_now_add=True) # renaming default date_joined field

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]

