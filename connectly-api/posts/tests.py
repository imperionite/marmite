from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Follow, Like

User = get_user_model()

class FeedViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password1')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password2')
        self.user3 = User.objects.create_user(username='user3', email='user3@example.com', password='password3')
        self.post1 = Post.objects.create(author=self.user1, content='Post 1 content')
        self.post2 = Post.objects.create(author=self.user2, content='Post 2 content')
        self.post3 = Post.objects.create(author=self.user3, content='Post 3 content')
        Follow.objects.create(follower=self.user1, following=self.user2)
        Like.objects.create(user=self.user1, post=self.post3)

    def test_feed_view_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_feed_view_followed_filter(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('feed') + '?filter=followed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['author_username'], 'user2')

    def test_feed_view_liked_filter(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('feed') + '?filter=liked')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['author_username'], 'user3')

    def test_feed_view_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)