from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from journal.models import Task, TaskCategory


NUMBER_OF_SHARED_TASKS = 10
NUMBER_OF_USER_PRIVATE_TASKS = 5
NUMBER_OF_SHARED_COMPLETED_TASKS = 7
NUMBER_OF_USER_PRIVATE_COMPLETED_TASKS = 3
NUMBER_OF_ARCHIVED_SHARED_TASKS = 4
TOTAL_ACTIVE_USER_TASKS = NUMBER_OF_SHARED_TASKS + NUMBER_OF_USER_PRIVATE_TASKS
TOTAL_COMPLETED_USER_TASKS = NUMBER_OF_SHARED_COMPLETED_TASKS + NUMBER_OF_USER_PRIVATE_COMPLETED_TASKS


class TaskListViewTest(TestCase):
    username = "testuser"
    password = "password"
    super_name = "superuser"
    super_password = "superword"

    @classmethod
    def setUpTestData(cls):
        # Create test users
        new_user = get_user_model().objects.create_user(cls.username, password=cls.password)
        super_user = get_user_model().objects.create_user(cls.super_name, password=cls.super_password,
                                                          is_superuser=True)

        # Add category
        category = TaskCategory.objects.create(title="New  category")

        # Add shared tasks
        for i_task in range(NUMBER_OF_SHARED_TASKS):
            Task.objects.create(title=f"Shared task {i_task}", author=new_user, body=f"Shared task {i_task} body",
                                category=category)
        # Add completed shared tasks
        for i_task in range(NUMBER_OF_SHARED_COMPLETED_TASKS):
            Task.objects.create(title=f"Completed shared task {i_task}", author=new_user,
                                body=f"Completed shared task {i_task} body",
                                category=category, is_completed=True)
        # Add completed user private tasks
        for i_task in range(NUMBER_OF_USER_PRIVATE_COMPLETED_TASKS):
            Task.objects.create(title=f"Completed private task {i_task} of {new_user.username}", author=new_user,
                                body=f"Completed private task {i_task} body",
                                category=category, is_completed=True, is_private=True)
        # Add active private user tasks
        for i_task in range(NUMBER_OF_USER_PRIVATE_TASKS):
            Task.objects.create(title=f"Private task {i_task} of {new_user.username}", author=new_user,
                                body=f"Private task {i_task} body",
                                category=category, is_private=True, is_completed=False)
        # Add archived shared tasks
        for i_task in range(NUMBER_OF_ARCHIVED_SHARED_TASKS):
            Task.objects.create(title=f"Archived shared task {i_task}", author=new_user,
                                body=f"Archived shared task {i_task} body",
                                category=category, is_private=False, is_archived=True)

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
        self.assertEqual(len(response.context["task_list"]), TOTAL_ACTIVE_USER_TASKS)

    def test_task_list_view_task_count_with_hide_private_filter(self):
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)
        # Go to list page with "hide private" filter
        url = reverse("journal:task_list") + "?hide_private=true"
        response = self.client.get(url)
        # Check tasks count on the page
        self.assertEqual(len(response.context["task_list"]), NUMBER_OF_SHARED_TASKS)

    def test_task_list_view_private_task_count(self):
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)
        # Go to private task list page
        url = reverse("journal:private_task_list")
        response = self.client.get(url)
        # Check tasks count on the page
        self.assertEqual(len(response.context["private_task_list"]), NUMBER_OF_USER_PRIVATE_TASKS)

    def test_task_list_view_completed_task_count(self):
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)
        # Go to private task list page
        url = reverse("journal:completed_task_list")
        response = self.client.get(url)
        # Check tasks count on the page
        self.assertEqual(len(response.context["completed_task_list"]), TOTAL_COMPLETED_USER_TASKS)
