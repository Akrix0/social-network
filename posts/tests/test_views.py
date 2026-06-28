from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post, PostLike, Comment

User = get_user_model()


class PostViewsTest(TestCase):

    def setUp(self):
        self.author = User.objects.create_user("author", password="pass12345")
        self.other = User.objects.create_user("other", password="pass12345")
        self.client = Client()
        self.client.login(username="author", password="pass12345")
        self.post = Post.objects.create(
            author=self.author,
            title="My post",
            content="Post body",
        )

    def test_posts_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("posts_list"))
        self.assertEqual(response.status_code, 302)

    def test_post_detail_shows_post(self):
        response = self.client.get(reverse("post_detail", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My post")

    def test_create_post(self):
        response = self.client.post(reverse("post_create"), {
            "title": "New post",
            "content": "New content",
        })
        self.assertEqual(Post.objects.filter(title="New post").count(), 1)
        post = Post.objects.get(title="New post")
        self.assertRedirects(response, reverse("post_detail", args=[post.pk]))

    def test_edit_post_by_author(self):
        response = self.client.post(
            reverse("post_edit", args=[self.post.pk]),
            {"title": "Updated", "content": "Updated body"},
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated")
        self.assertRedirects(response, reverse("post_detail", args=[self.post.pk]))

    def test_edit_post_forbidden_for_non_author(self):
        self.client.logout()
        self.client.login(username="other", password="pass12345")
        response = self.client.get(reverse("post_edit", args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)

    def test_delete_post(self):
        response = self.client.post(reverse("post_delete", args=[self.post.pk]))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
        self.assertRedirects(response, reverse("posts_list"))

    def test_add_comment_on_post_detail(self):
        response = self.client.post(
            reverse("post_detail", args=[self.post.pk]),
            {"content": "Great post!"},
        )
        self.assertEqual(Comment.objects.filter(post=self.post).count(), 1)
        self.assertRedirects(response, reverse("post_detail", args=[self.post.pk]))


class PostLikeAPITest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("liker", password="pass12345")
        self.author = User.objects.create_user("author", password="pass12345")
        self.post = Post.objects.create(
            author=self.author,
            title="Like me",
            content="Content",
        )
        self.client = Client()
        self.client.login(username="liker", password="pass12345")

    def test_toggle_like_creates_and_removes_like(self):
        url = reverse("toggle-post-like-api", args=[self.post.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["liked"])
        self.assertEqual(data["likes_count"], 1)
        self.assertTrue(PostLike.objects.filter(user=self.user, post=self.post).exists())

        response = self.client.post(url)
        data = response.json()
        self.assertFalse(data["liked"])
        self.assertEqual(data["likes_count"], 0)
