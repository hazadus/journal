from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

from journal.models import Task, TaskCategory


NUMBER_OF_SHARED_TASKS = 10


class JournalAPITest(APITestCase):
    """
    Test Journal DRF API.
    """
    username = "testuser"
    password = "password"
    new_user = None

    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.new_user = get_user_model().objects.create_user(cls.username, password=cls.password)

        # Add category
        category = TaskCategory.objects.create(title="New category")

        # Add shared tasks
        for i_task in range(NUMBER_OF_SHARED_TASKS):
            Task.objects.create(title=f"Shared task {i_task}", author=cls.new_user, body=f"Shared task {i_task} body",
                                category=category)

    def test_task_acquaint_api(self):
        """
        Ensure that acquaintance endpoint located where expected and works.
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)

        task = Task.objects.first()
        url = f"/journal/tasks/api/v1/task/{task.pk}/acquaint/"
        response = self.client.get(url)
        self.assertEqual(task.users_acquainted.all()[0], self.new_user)
