from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Follow

User = get_user_model()


class GetFriendsTest(TestCase):

    def setUp(self):
        self.alice = User.objects.create_user("alice", password="pass12345")
        self.bob = User.objects.create_user("bob", password="pass12345")
        self.carol = User.objects.create_user("carol", password="pass12345")

    def test_mutual_follow_returns_friend(self):
        Follow.objects.create(follower=self.alice, following=self.bob)
        Follow.objects.create(follower=self.bob, following=self.alice)

        friends = list(self.alice.get_friends())
        self.assertEqual(len(friends), 1)
        self.assertEqual(friends[0], self.bob)

    def test_one_way_follow_is_not_friend(self):
        Follow.objects.create(follower=self.alice, following=self.bob)

        self.assertEqual(self.alice.get_friends().count(), 0)

    def test_is_friends_classmethod(self):
        Follow.objects.create(follower=self.alice, following=self.carol)
        Follow.objects.create(follower=self.carol, following=self.alice)

        self.assertTrue(Follow.is_friends(self.alice, self.carol))
        self.assertFalse(Follow.is_friends(self.alice, self.bob))
