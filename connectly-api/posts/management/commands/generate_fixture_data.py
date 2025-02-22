import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Post, Comment, Like  # Import your models

class Command(BaseCommand):
    help = 'Generates fixture data with hashed passwords'

    def handle(self, *args, **options):
        users = []
        posts = []
        comments = []
        likes = []

        # Create users with hashed passwords (Admin user first)
        user0 = User.objects.create_superuser(username='user0', email='user0@example.com', password='passworD1#')
        users.append({"model": "posts.user", "pk": user0.pk, "fields": {"username": user0.username, "email": user0.email, "is_superuser": user0.is_superuser, "is_staff": user0.is_staff}})

        for i in range(1, 5):  # Create 4 regular users (user1 to user4)
            user = User.objects.create_user(username=f'user{i}', email=f'user{i}@example.com', password='passworD1#')
            users.append({"model": "posts.user", "pk": user.pk, "fields": {"username": user.username, "email": user.email}})

        # Create posts (6 posts)
        post1 = Post.objects.create(content="Post 1 content by user0", author=user0)
        posts.append({"model": "posts.post", "pk": post1.pk, "fields": {"content": post1.content, "author": user0.pk}})

        user_list = [user0] # user0 is already in the list
        for i in range(1, 5):
            user_list.append(User.objects.get(username=f'user{i}'))

        post2 = Post.objects.create(content="Post 2 content by user1", author=user_list[1])
        posts.append({"model": "posts.post", "pk": post2.pk, "fields": {"content": post2.content, "author": user_list[1].pk}})

        post3 = Post.objects.create(content="Post 3 content by user2", author=user_list[2])
        posts.append({"model": "posts.post", "pk": post3.pk, "fields": {"content": post3.content, "author": user_list[2].pk}})

        post4 = Post.objects.create(content="Post 4 content by user3", author=user_list[3])
        posts.append({"model": "posts.post", "pk": post4.pk, "fields": {"content": post4.content, "author": user_list[3].pk}})

        post5 = Post.objects.create(content="Post 5 content by user4", author=user_list[4])
        posts.append({"model": "posts.post", "pk": post5.pk, "fields": {"content": post5.content, "author": user_list[4].pk}})

        post6 = Post.objects.create(content="Post 6 content by user0", author=user0)
        posts.append({"model": "posts.post", "pk": post6.pk, "fields": {"content": post6.content, "author": user0.pk}})


        # Create comments (5 comments)
        comment1 = Comment.objects.create(content="Comment 1 on post 1 by user1", user=user_list[1], post=post1)
        comments.append({"model": "posts.comment", "pk": comment1.pk, "fields": {"content": comment1.content, "user": user_list[1].pk, "post": post1.pk}})

        comment2 = Comment.objects.create(content="Comment 2 on post 1 by user2", user=user_list[2], post=post1)
        comments.append({"model": "posts.comment", "pk": comment2.pk, "fields": {"content": comment2.content, "user": user_list[2].pk, "post": post1.pk}})

        comment3 = Comment.objects.create(content="Comment on post 2 by user0", user=user0, post=post2)
        comments.append({"model": "posts.comment", "pk": comment3.pk, "fields": {"content": comment3.content, "user": user0.pk, "post": post2.pk}})

        comment4 = Comment.objects.create(content="Another comment on post 2 by user3", user=user_list[3], post=post2)
        comments.append({"model": "posts.comment", "pk": comment4.pk, "fields": {"content": comment4.content, "user": user_list[3].pk, "post": post2.pk}})

        comment5 = Comment.objects.create(content="Comment on post 3 by user4", user=user_list[4], post=post3)
        comments.append({"model": "posts.comment", "pk": comment5.pk, "fields": {"content": comment5.content, "user": user_list[4].pk, "post": post3.pk}})


        # Create likes (3 likes)
        like1 = Like.objects.create(user=user_list[1], post=post1)
        likes.append({"model": "posts.like", "pk": like1.pk, "fields": {"user": user_list[1].pk, "post": post1.pk}})

        like2 = Like.objects.create(user=user_list[2], post=post1)
        likes.append({"model": "posts.like", "pk": like2.pk, "fields": {"user": user_list[2].pk, "post": post1.pk}})

        like3 = Like.objects.create(user=user0, post=post3)
        likes.append({"model": "posts.like", "pk": like3.pk, "fields": {"user": user0.pk, "post": post3.pk}})

        # Create unlikes (2 unlikes - these are actually likes that will be deleted)
        unlike1 = Like.objects.create(user=user0, post=post2) # This like will be deleted to simulate unlike
        likes.append({"model": "posts.like", "pk": unlike1.pk, "fields": {"user": user0.pk, "post": post2.pk}})

        unlike2 = Like.objects.create(user=user_list[3], post=post4) # This like will be deleted to simulate unlike
        likes.append({"model": "posts.like", "pk": unlike2.pk, "fields": {"user": user_list[3].pk, "post": post4.pk}})


        # Combine all data
        fixture_data = users + posts + comments + likes

        # Write to JSON file
        with open('posts/fixtures/initial_data.json', 'w') as f:
            json.dump(fixture_data, f, indent=2)

        self.stdout.write(self.style.SUCCESS('Fixture data generated successfully!'))