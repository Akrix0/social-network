from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from boards.models import Board

User = get_user_model()


class BoardViewsTest(TestCase):

    def setUp(self):
        self.creator = User.objects.create_user("creator", password="pass12345")
        self.member = User.objects.create_user("member", password="pass12345")
        self.board = Board.objects.create(
            title="Django Fans",
            description="Board for Django lovers",
            creator=self.creator,
        )
        self.client = Client()

    def test_join_board_adds_member(self):
        self.client.login(username="member", password="pass12345")
        response = self.client.post(
            reverse("join_board", args=[self.board.slug])
        )
        self.assertTrue(self.board.members.filter(pk=self.member.pk).exists())
        self.assertRedirects(response, reverse("board_detail", args=[self.board.slug]))

    def test_boards_list_requires_login(self):
        response = self.client.get(reverse("boards_list"))
        self.assertEqual(response.status_code, 302)

    def test_board_detail_requires_membership(self):
        self.client.login(username="member", password="pass12345")
        response = self.client.get(reverse("board_detail", args=[self.board.slug]))
        self.assertRedirects(response, reverse("boards_list"))
