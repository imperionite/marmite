from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _

"""
# Like Relationship (Many-to-Many)
# Instead of using a ManyToManyField, we use an explicit through model (Like), allowing us to store extra metadata like the created_at timestamp.
# The unique_together = ("user", "post") constraint prevents duplicate likes, ensuring a user can like a post only once.
# Comment Relationship (One-to-Many)
# Each Comment references:
# A User (who wrote the comment).
# A Post (the post being commented on).
# The related_name="comments" allows easy access to all comments related to a post (post.comments.all()).
"""

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
    """Model representing a post created by a user."""
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on Post {self.post.id}"
    

class Comment(models.Model):
    """Model representing a comment on a post."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments") 
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments")  # The post this comment belongs to)
    content = models.TextField() # change the field name from text
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"


class Like(models.Model):
    """Model representing a like on a post."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")  # The user who liked a post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")  # The liked post
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ("user", "post")  # Ensures a user can like a post only once

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"


