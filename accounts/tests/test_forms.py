from django.test import TestCase
from accounts.forms import RegistrationStep1Form


class RegistrationStep1FormTest(TestCase):

    def test_valid_form(self):
        form = RegistrationStep1Form(data={
            "username": "roman",
            "email": "roman@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form = RegistrationStep1Form(data={
            "username": "roman",
            "email": "roman@example.com",
            "password1": "StrongPass123!",
            "password2": "DifferentPass123!",
        })
        self.assertFalse(form.is_valid())
