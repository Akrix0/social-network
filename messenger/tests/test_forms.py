from django.test import TestCase
from django.contrib.auth import get_user_model
from messenger.models import Chat, Message
from messenger.forms import MessageForm

User = get_user_model()


class MessageFormTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user("user1", password="pass12345")
        self.user2 = User.objects.create_user("user2", password="pass12345")
        self.chat = Chat.objects.create(is_group=False)
        self.chat.users.add(self.user1, self.user2)
        self.parent = Message.objects.create(
            chat=self.chat,
            user=self.user1,
            text="Parent message",
        )

    def test_reply_to_valid_message(self):
        form = MessageForm(
            {"text": "Reply", "reply_to": self.parent.pk},
            chat=self.chat,
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["reply_to"], self.parent)

    def test_reply_to_invalid_message_id(self):
        form = MessageForm(
            {"text": "Reply", "reply_to": 99999},
            chat=self.chat,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("reply_to", form.errors)

    def test_reply_to_message_from_other_chat_rejected(self):
        other_chat = Chat.objects.create(is_group=False)
        other_chat.users.add(self.user1, self.user2)
        foreign = Message.objects.create(
            chat=other_chat,
            user=self.user1,
            text="Other chat",
        )
        form = MessageForm(
            {"text": "Reply", "reply_to": foreign.pk},
            chat=self.chat,
        )
        self.assertFalse(form.is_valid())
