from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post, PostLike, Comment

User = get_user_model()


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("author", password="pass12345")

    def test_post_str(self):
        post = Post.objects.create(
            author=self.user,
            title="Test title",
            content="Test content",
        )
        self.assertEqual(str(post), "Test title")

    def test_unique_post_like(self):
        post = Post.objects.create(
            author=self.user,
            title="Likes",
            content="Content",
        )
        PostLike.objects.create(user=self.user, post=post)
        with self.assertRaises(Exception):
            PostLike.objects.create(user=self.user, post=post)


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("author", password="pass12345")
        self.post = Post.objects.create(
            author=self.user,
            title="Post",
            content="Content",
        )

    def test_comment_str_contains_username(self):
        comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            content="Nice post",
        )
        self.assertIn("author", str(comment))
