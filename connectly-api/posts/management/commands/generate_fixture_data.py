import os
import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from ...models import Post, Comment, Like, Follow

User = get_user_model()

class Command(BaseCommand):
    help = 'Generates fixture data with hashed passwords, roles, and post privacy'

    def handle(self, *args, **options):
        users = []
        posts = []
        comments = []
        likes = []
        follows = []

        # Create users with hashed passwords and roles (Admin user first)
        user0, created = User.objects.get_or_create(
            email='user0@example.com',
            defaults={
                'username': 'user0',
                'password': make_password('passworD1#'),
                'is_superuser': True,
                'is_staff': True,
                'role': 'admin'  # Set admin role
            }
        )
        users.append({
            "model": "posts.user",
            "pk": user0.pk,
            "fields": {
                "username": user0.username,
                "email": user0.email,
                "is_superuser": user0.is_superuser,
                "is_staff": user0.is_staff,
                "role": user0.role,
                "created_at": user0.created_at.isoformat()
            }
        })

        # Check for existing "admin" user and set role
        try:
            admin_user = User.objects.get(username='admin')
            admin_user.role = 'admin'
            admin_user.save()
            users.append({
                "model": "posts.user",
                "pk": admin_user.pk,
                "fields": {
                    "username": admin_user.username,
                    "email": admin_user.email,
                    "role": admin_user.role,
                    "created_at": admin_user.created_at.isoformat()
                }
            })
        except User.DoesNotExist:
            pass  # User "admin" doesn't exist, continue

        for i in range(1, 5):  # Create 4 regular users (user1 to user4)
            user, created = User.objects.get_or_create(
                email=f'user{i}@example.com',
                defaults={
                    'username': f'user{i}',
                    'password': make_password('passworD1#'),
                    'role': 'user'  # Set user role
                }
            )
            users.append({
                "model": "posts.user",
                "pk": user.pk,
                "fields": {
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "created_at": user.created_at.isoformat()
                }
            })

        user_list = User.objects.all()  # Get all users dynamically

        # Create posts (6 posts) with privacy settings
        post_data = [
            {"content": "Post 1 content by user0", "author": user0, "privacy": "public"},
            {"content": "Post 2 content by user1", "author": user_list[1], "privacy": "private"},
            {"content": "Post 3 content by user2", "author": user_list[2], "privacy": "public"},
            {"content": "Post 4 content by user3", "author": user_list[3], "privacy": "private"},
            {"content": "Post 5 content by user4", "author": user_list[4], "privacy": "public"},
            {"content": "Post 6 content by user0", "author": user0, "privacy": "private"},
        ]
        for data in post_data:
            post, created = Post.objects.get_or_create(**data)
            if created:
                posts.append({
                    "model": "posts.post",
                    "pk": post.pk,
                    "fields": {
                        "content": post.content,
                        "author": post.author.pk,
                        "privacy": post.privacy, # add privacy
                        "created_at": post.created_at.isoformat()
                    }
                })

        # Create comments (5 comments)
        comment_data = [
            {"content": "Comment 1 on post 1 by user1", "user": user_list[1], "post": Post.objects.get(id=1)},
            {"content": "Comment 2 on post 1 by user2", "user": user_list[2], "post": Post.objects.get(id=1)},
            {"content": "Comment on post 2 by user0", "user": user0, "post": Post.objects.get(id=2)},
            {"content": "Another comment on post 2 by user3", "user": user_list[3], "post": Post.objects.get(id=2)},
            {"content": "Comment on post 3 by user4", "user": user_list[4], "post": Post.objects.get(id=3)},
        ]
        for data in comment_data:
            comment, created = Comment.objects.get_or_create(**data)
            if created:
                comments.append({
                    "model": "posts.comment",
                    "pk": comment.pk,
                    "fields": {
                        "content": comment.content,
                        "user": comment.user.pk,
                        "post": comment.post.pk,
                        "created_at": comment.created_at.isoformat()
                    }
                })

        # Create likes (3 likes)
        like_data = [
            {"user": user_list[1], "post": Post.objects.get(id=1)},
            {"user": user_list[2], "post": Post.objects.get(id=1)},
            {"user": user0, "post": Post.objects.get(id=3)},
        ]
        for data in like_data:
            like, created = Like.objects.get_or_create(**data)
            if created:
                likes.append({
                    "model": "posts.like",
                    "pk": like.pk,
                    "fields": {
                        "user": like.user.pk,
                        "post": like.post.pk,
                        "created_at": like.created_at.isoformat()
                    }
                })

        # Create follows (2 follows)
        follow_data = [
            {"follower": user0, "following": user_list[1]},
            {"follower": user_list[1], "following": user_list[2]},
        ]
        for data in follow_data:
            follow, created = Follow.objects.get_or_create(**data)
            if created:
                follows.append({
                    "model": "posts.follow",
                    "pk": follow.pk,
                    "fields": {
                        "follower": follow.follower.pk,
                        "following": follow.following.pk,
                        "created_at": follow.created_at.isoformat()
                    }
                })

        # Combine all data
        fixture_data = users + posts + comments + likes + follows

        # Dynamically generate the absolute path
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        FIXTURES_DIR = os.path.join(BASE_DIR, 'connectly-api', 'posts', 'fixtures')
        FILE_PATH = os.path.join(FIXTURES_DIR, 'initial_data.json')

        # Ensure the fixtures directory exists
        os.makedirs(FIXTURES_DIR, exist_ok=True)

        # Write to JSON file
        with open(FILE_PATH, 'w') as f:
            json.dump(fixture_data, f, indent=2)

        self.stdout.write(self.style.SUCCESS('Fixture data generated successfully!'))