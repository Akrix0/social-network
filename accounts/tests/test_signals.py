from django.test import TestCase
from django.urls import reverse
from accounts.models import Follow
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()


class FollowNotificationSignalTest(TestCase):

    def setUp(self):
        self.follower = User.objects.create_user("follower", password="pass12345")
        self.following = User.objects.create_user("following", password="pass12345")

    def test_follow_creates_notification_with_follower_profile_url(self):
        Follow.objects.create(follower=self.follower, following=self.following)

        notification = Notification.objects.get(
            to_user=self.following,
            event_type=Notification.EventType.NEW_FOLLOWER,
        )
        expected_url = reverse("user_detail", kwargs={"slug": self.follower.slug})
        self.assertEqual(notification.target_url, expected_url)
        self.assertEqual(notification.from_user, self.follower)

    def test_self_follow_does_not_create_notification(self):
        Follow.objects.create(follower=self.follower, following=self.follower)
        self.assertEqual(Notification.objects.count(), 0)
