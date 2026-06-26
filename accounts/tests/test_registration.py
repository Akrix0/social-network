from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationFlowTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_step1_creates_user_and_stores_session_id_not_password(self):
        response = self.client.post(reverse("register_step1"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn("registration_user_id", self.client.session)
        self.assertNotIn("registration_data", self.client.session)

        user = User.objects.get(username="newuser")
        self.assertEqual(self.client.session["registration_user_id"], user.pk)
        self.assertTrue(user.check_password("SecurePass123!"))

    def test_step2_without_step1_redirects(self):
        response = self.client.get(reverse("register_step2"))
        self.assertRedirects(response, reverse("register_step1"))

    def test_step2_complete_later_logs_in_user(self):
        self.client.post(reverse("register_step1"), {
            "username": "lateruser",
            "email": "later@example.com",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        })
        response = self.client.post(reverse("register_step2"), {
            "action": "later",
        })
        user = User.objects.get(username="lateruser")
        self.assertRedirects(response, reverse("user_detail", args=[user.slug]))

    def test_step2_complete_profile_updates_user(self):
        self.client.post(reverse("register_step1"), {
            "username": "fulluser",
            "email": "full@example.com",
            "password1": "SecurePass123!",
            "password2": "SecurePass123!",
        })
        response = self.client.post(reverse("register_step2"), {
            "first_name": "Full",
            "last_name": "User",
            "bio": "Hello world",
            "birthday": "2000-01-01",
        })
        user = User.objects.get(username="fulluser")
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Full")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.bio, "Hello world")
        self.assertRedirects(response, reverse("user_detail", args=[user.slug]))
