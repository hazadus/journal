from django.urls import reverse
from django.test import TestCase

from users.models import CustomUser
from core.models import Notification


class UsersSignalsTest(TestCase):
    username = "testuser"
    password = "password"
    admin_username = "admin"
    admin_password = "password"

    @classmethod
    def setUpTestData(cls):
        new_user = CustomUser.objects.create_user(
            cls.username, password=cls.password
        )
        new_admin = CustomUser.objects.create_user(
            cls.admin_username, password=cls.admin_password, is_superuser=True,
        )

    def test_user_login_logout_signals(self):
        """
        Ensure that notifications are created on user login and logout
        """
        # Login
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)
        # We have one superuser, so one notification should be created:
        self.assertEqual(
            Notification.objects.count(), 1
        )
        url = reverse("logout")
        response = self.client.get(url)
        # Second notification should be created after logout;
        self.assertEqual(
            Notification.objects.count(), 2
        )
