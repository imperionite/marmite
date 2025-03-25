import os
import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from ...models import Post, Comment, Like, Follow
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Generates fixture data with hashed passwords, roles, and post privacy'

    def handle(self, *args, **options):
        users = []
        posts = []
        comments = []
        likes = []
        follows = []

        # ======================
        #  Check Seeding Conditions
        # ======================
        if not (
            User.objects.filter(username='admin').count() == 1 and
            not Post.objects.exists() and
            not Comment.objects.exists() and
            not Like.objects.exists()
        ):
            self.stdout.write(self.style.WARNING(
                'Seeding conditions not satisfied. Skipping fixture generation.'
            ))
            return

        # ======================
        #  Create Users
        # ======================
        # Create user0 as admin
        user0, created = User.objects.get_or_create(
            username='user0',
            defaults={
                'email': 'user0@example.com',
                'password': make_password('passworD1#'),
                'is_superuser': False, # not superuser
                'is_staff': True,
                'role': 'admin'  # admin role
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

        # Create regular users (user1 to user19)
        for i in range(1, 20):
            user, created = User.objects.get_or_create(
                email=f'user{i}@example.com',
                defaults={
                    'username': f'user{i}',
                    'password': make_password('passworD1#'),
                    'role': 'user'
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

        # ======================
        #  Create Posts (50 posts)
        # ======================
        existing_post_authors = set()
        for i in range(1, 51):
            author = random.choice(users[1:])  # Exclude admin
            privacy = random.choice(["public", "private"])
            
            # Create post only if content is unique (optional)
            post_content = f"Post {i} content by {author['fields']['username']}"
            if not Post.objects.filter(content=post_content).exists():
                post = Post(
                    content=post_content,
                    author=User.objects.get(pk=author["pk"]),
                    privacy=privacy
                )
                post.save()
                posts.append({
                    "model": "posts.post",
                    "pk": post.pk,
                    "fields": {
                        "content": post.content,
                        "author": post.author.pk,
                        "privacy": post.privacy,
                        "created_at": post.created_at.isoformat()
                    }
                })

        # ======================
        #  Create Comments (100 comments)
        # ======================
        comment_set = set()  # Track user-post pairs
        for i in range(1, 101):
            user = random.choice(users)
            post = random.choice(posts)
            
            # Ensure unique comment per user-post combo
            comment_key = (user["pk"], post["pk"])
            if comment_key not in comment_set:
                comment = Comment(
                    content=f"Comment {i} by {user['fields']['username']}",
                    user=User.objects.get(pk=user["pk"]),
                    post=Post.objects.get(pk=post["pk"])
                )
                comment.save()
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
                comment_set.add(comment_key)

        # ======================
        #  Create Likes (200 likes)
        # ======================
        like_pairs = set()  # Track user-post pairs
        like_count = 0
        while like_count < 200:
            user = random.choice(users)
            post = random.choice(posts)
            
            # Check both database and current batch
            user_post_pair = (user["pk"], post["pk"])
            
            if (
                not Like.objects.filter(user=user["pk"], post=post["pk"]).exists()
                and user_post_pair not in like_pairs
            ):
                like = Like(
                    user=User.objects.get(pk=user["pk"]),
                    post=Post.objects.get(pk=post["pk"])
                )
                like.save()
                likes.append({
                    "model": "posts.like",
                    "pk": like.pk,
                    "fields": {
                        "user": like.user.pk,
                        "post": like.post.pk,
                        "created_at": like.created_at.isoformat()
                    }
                })
                like_pairs.add(user_post_pair)
                like_count += 1

        # ======================
        #  Create Follows (100 follows)
        # ======================
        follow_pairs = set()  # Track follower-following pairs
        follow_count = 0
        while follow_count < 100:
            follower = random.choice(users)
            following = random.choice(users)
            
            # Skip self-follows and duplicates
            follower_pk = follower["pk"]
            following_pk = following["pk"]
            if (
                follower_pk != following_pk
                and not Follow.objects.filter(follower=follower_pk, following=following_pk).exists()
                and (follower_pk, following_pk) not in follow_pairs
            ):
                follow = Follow(
                    follower=User.objects.get(pk=follower_pk),
                    following=User.objects.get(pk=following_pk)
                )
                follow.save()
                follows.append({
                    "model": "posts.follow",
                    "pk": follow.pk,
                    "fields": {
                        "follower": follow.follower.pk,
                        "following": follow.following.pk,
                        "created_at": follow.created_at.isoformat()
                    }
                })
                follow_pairs.add((follower_pk, following_pk))
                follow_count += 1

        # ======================
        #  Save to Fixture File
        # ======================
        fixture_data = users + posts + comments + likes + follows

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        FIXTURES_DIR = os.path.join(BASE_DIR, 'fixtures')
        FILE_PATH = os.path.join(FIXTURES_DIR, 'initial_data.json')

        os.makedirs(FIXTURES_DIR, exist_ok=True)

        with open(FILE_PATH, 'w') as f:
            json.dump(fixture_data, f, indent=2)

        self.stdout.write(self.style.SUCCESS('Fixture data generated successfully!'))
