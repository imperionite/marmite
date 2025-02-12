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
    """Model representing a post created by a user."""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  # A user can have multiple posts
    content = models.TextField()  # Post content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was created

    def __str__(self):
        return f"Post by {self.author.username} - {self.created_at}"
    

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)  # User who liked
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)  # Liked post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when liked
    
    class Meta:
        unique_together = ('user', 'post')  # Ensure a user can like a post only once
    
    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"






#

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    """Model representing a post created by a user."""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  # A user can have multiple posts
    content = models.TextField()  # Post content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was created

    def __str__(self):
        return f"Post by {self.author.username} - {self.created_at}"


class Comment(models.Model):
    """Model representing a comment on a post."""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  # User who wrote the comment
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")  # The post this comment belongs to
    text = models.TextField()  # The content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the comment was created

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.id}"


class Like(models.Model):
    """Model representing a like on a post."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")  # The user who liked a post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")  # The liked post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the like was added

    class Meta:
        unique_together = ("user", "post")  # Ensures a user can like a post only once

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"

