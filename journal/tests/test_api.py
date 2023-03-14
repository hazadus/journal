import json

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from core.models import Notification
from journal.models import Task, TaskCategory, Comment


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
        Ensure that acquaintance endpoint located where expected and works - user gets acquainted with task itself
        and it's comments.
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)

        task = Task.objects.first()
        comment = Comment.objects.create(
            task=task, author=self.new_user, body="New comment"
        )
        url = f"/journal/tasks/api/v1/task/{task.pk}/acquaint/"
        response = self.client.get(url)
        self.assertEqual(task.users_acquainted.all()[0], self.new_user)
        self.assertEqual(task.comments.all()[0].users_acquainted.all()[0], self.new_user)

    def test_comment_create_api(self):
        """
        Test comment creation endpoint.
        Ensures that comment is properly created, authors gets acquainted with his new comment, task is completed,
        notifications are sent.
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)
        task = Task.objects.first()
        url = "/journal/tasks/api/v1/comment/"
        body = "New comment"
        response = self.client.post(url, data={
            "newComment": {
                "author": self.new_user.pk,
                "task": task.pk,
                "body": body,
            },
            "isCompleteTask": True,
        }, format="json")

        comment = Comment.objects.first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(comment.body, body)
        self.assertEqual(comment.task.is_completed, True)
        self.assertEqual(json.loads(response.content), {"author": 1, "body": "New comment", "id": 1, "task": 10})
        self.assertEqual(comment.users_acquainted.all()[0], self.new_user)
        # There should be 2 notifications: one about comment added, and one about task completed:
        self.assertEqual(Notification.objects.count(), 2)

    def test_comment_create_for_wrong_task_api(self):
        """
        Test comment creation endpoint with wrong task ID.
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)
        task = Task.objects.first()
        url = "/journal/tasks/api/v1/comment/"
        body = "New comment"
        print("Try to make wrong request on purpose:")
        response = self.client.post(url, data={
            "newComment": {
                "author": self.new_user.pk,
                "task": 99,
                "body": body,
            },
            "isCompleteTask": False,
        }, format="json")
        self.assertEqual(response.status_code, 400)

    def test_comment_edit_api(self):
        """
        Test comment editing endpoint.
        Try to edit by comment author.
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password}, follow=True)

        task = Task.objects.first()
        comment = Comment.objects.create(task=task, author=self.new_user, body="Comment to edit")

        url = f"/journal/tasks/api/v1/comment/{comment.id}/edit/"
        new_body = "Changed comment body"
        response = self.client.post(url, data={"body": new_body, }, format="json")
        self.assertEqual(response.status_code, 200)

        # Check if DB was actually updated
        updated_comment = Comment.objects.get(pk=comment.pk)
        self.assertEqual(updated_comment.body, new_body)

    def test_comment_edit_api_by_another_user(self):
        """
        Test comment editing endpoint.
        Try to edit comment by another user (not by it's author).
        """
        username = "anotheruser"
        password = "password"

        another_user = get_user_model().objects.create_user(username=username, password=password)
        url = reverse("login")
        self.client.post(url, {"username": username, "password": password}, follow=True)

        task = Task.objects.first()
        comment = Comment.objects.create(task=task, author=self.new_user, body="Comment to edit")

        # Try to edit comment by wrong user
        url = f"/journal/tasks/api/v1/comment/{comment.id}/edit/"
        new_body = "Changed comment body"
        response = self.client.post(url, data={"body": new_body, }, format="json")
        self.assertEqual(response.status_code, 400)
