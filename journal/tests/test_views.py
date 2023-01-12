from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from journal.models import Task, TaskCategory


NUMBER_OF_SHARED_TASKS = 10
NUMBER_OF_USER_PRIVATE_TASKS = 5
NUMBER_OF_USER_COMPLETED_TASKS = 7
TOTAL_NUMBER_USER_TASKS = NUMBER_OF_SHARED_TASKS + NUMBER_OF_USER_PRIVATE_TASKS


class TaskListViewTest(TestCase):
    username = "testuser"
    email = "newuser@email.com"
    password = "password"

    @classmethod
    def setUpTestData(cls):
        # Create test user
        new_user = get_user_model().objects.create_user(cls.username, cls.email, password=cls.password)

        # Add category
        category = TaskCategory.objects.create(title="New  category")

        # Add shared tasks
        for i_task in range(NUMBER_OF_SHARED_TASKS):
            Task.objects.create(title=f"Task {i_task}", author=new_user, body=f"Task {i_task} body",
                                category=category)
        # Add completed shared tasks
        for i_task in range(NUMBER_OF_SHARED_TASKS):
            Task.objects.create(title=f"Completed task {i_task}", author=new_user,
                                body=f"Completed task {i_task} body",
                                category=category, is_completed=True)
        # TODO: add archived tasks
        # Add private tasks
        for i_task in range(NUMBER_OF_USER_PRIVATE_TASKS):
            Task.objects.create(title=f"Provate task {i_task}", author=new_user,
                                body=f"Provate task {i_task} body",
                                category=category, is_private=True)

    def test_home_url(self):
        # Test the "/" URL of the site
        # Redirect when not logged in
        url = reverse("journal:task_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_correct_login(self):
        # Check login for `testuser`
        # After login must be redirected to task list
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)
        self.assertContains(response, "Журнал Дежурства")
        self.assertContains(response, "задачи")

    def test_task_list_view_task_count(self):
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)
        # Go to list page
        url = reverse("journal:task_list")
        response = self.client.get(url)
        # Check tasks count on the page
        self.assertEqual(len(response.context["task_list"]), TOTAL_NUMBER_USER_TASKS)
