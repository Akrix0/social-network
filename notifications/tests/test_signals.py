from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post
from notifications.models import Notification

User = get_user_model()


class PostNotificationSignalTest(TestCase):

    def setUp(self):
        self.author = User.objects.create_user("author", password="pass12345")
        self.friend = User.objects.create_user("friend", password="pass12345")
        from accounts.models import Follow
        Follow.objects.create(follower=self.author, following=self.friend)
        Follow.objects.create(follower=self.friend, following=self.author)

    def test_new_post_notifies_friend(self):
        post = Post.objects.create(
            author=self.author,
            title="Hello friends",
            content="Content",
        )
        self.assertTrue(
            Notification.objects.filter(
                to_user=self.friend,
                event_type=Notification.EventType.NEW_POST,
                target_id=post.pk,
            ).exists()
        )
