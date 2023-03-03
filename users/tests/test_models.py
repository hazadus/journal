from django.test import TestCase

from users.models import CustomUser


class CustomUserModelTest(TestCase):
    """
    Test CustomUser model.
    """
    username = "testuser"
    password = "password"

    @classmethod
    def setUpTestData(cls):
        new_user = CustomUser.objects.create_user(
            cls.username, password=cls.password
        )

    def test_custom_user_str(self):
        """
        Ensure that CustomUser is correctly represented by username when converted to string.
        """
        self.assertEqual(
            str(CustomUser.objects.first()), self.username
        )
