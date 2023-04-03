from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardViewTest(TestCase):
    """
    Test "core:dashboard" view (list of notifications for current user).
    """

    super_name = "superuser"
    super_password = "superword"

    @classmethod
    def setUpTestData(cls):
        super_user = get_user_model().objects.create_user(
            cls.super_name, password=cls.super_password, is_superuser=True
        )

    def test_dashboard_without_login(self):
        """
        Ensure "core:dashboard" view is not accessible without login.
        """
        # Redirect when not logged in
        url = reverse("core:dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_dashboard_notification_count(self):
        """
        Check number of notifications shown in "core:dashboard" view.
        """
        # Login as superuser
        url = reverse("login")
        response = self.client.post(
            url,
            {"username": self.super_name, "password": self.super_password},
            follow=True,
        )
        # Go to dashboard page
        url = reverse("core:dashboard")
        response = self.client.get(url)
        # Check notification count on the page: there should be only one - about admin's login:
        self.assertEqual(len(response.context["notifications"]), 1)

        # Check request with non-existend page number - should return last existing page
        url += "?page=10"
        response = self.client.get(url)
        self.assertEqual(len(response.context["notifications"]), 1)

        # Response in HTMX mode with non-existent page number should be empty:
        url += "&notifications_only=1"
        response = self.client.get(url)
        self.assertEqual(response.content, b"")
