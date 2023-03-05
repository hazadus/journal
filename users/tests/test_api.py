import json

from django.urls import reverse
from django.test import TestCase

from users.models import CustomUser


class UserAPITest(TestCase):
    """
    Test User DRF API endpoints.
    """
    username = "testuser"
    password = "password"

    @classmethod
    def setUpTestData(cls):
        new_user = CustomUser.objects.create_user(
            cls.username, password=cls.password
        )

    def test_logged_in_user_api(self):
        """
        Check that `logged_in_user_api` return info about logged in user.
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)
        response = self.client.get("/users/api/v1/logged_in_user/")
        self.assertEqual(json.loads(response.content)["username"], self.username)
        self.assertEqual(json.loads(response.content)["id"], 1)
