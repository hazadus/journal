from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from journal.models import Task, TaskCategory

NUMBER_OF_SHARED_TASKS = 10
NUMBER_OF_USER_PRIVATE_TASKS = 5
NUMBER_OF_SHARED_COMPLETED_TASKS = 7
NUMBER_OF_USER_PRIVATE_COMPLETED_TASKS = 3
NUMBER_OF_ARCHIVED_SHARED_TASKS = 4
TOTAL_ACTIVE_USER_TASKS = NUMBER_OF_SHARED_TASKS + NUMBER_OF_USER_PRIVATE_TASKS
TOTAL_COMPLETED_USER_TASKS = (
    NUMBER_OF_SHARED_COMPLETED_TASKS + NUMBER_OF_USER_PRIVATE_COMPLETED_TASKS
)


class TaskListViewTest(TestCase):
    """
    Test task list views.
    """

    username = "testuser"
    password = "password"
    super_name = "superuser"
    super_password = "superword"
    new_user = None

    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.new_user = get_user_model().objects.create_user(
            cls.username, password=cls.password
        )
        super_user = get_user_model().objects.create_user(
            cls.super_name, password=cls.super_password, is_superuser=True
        )

        # Add category
        category = TaskCategory.objects.create(title="New  category")

        # Add shared tasks
        for i_task in range(NUMBER_OF_SHARED_TASKS):
            Task.objects.create(
                title=f"Shared task {i_task}",
                author=cls.new_user,
                body=f"Shared task {i_task} body",
                category=category,
            )
        # Add completed shared tasks
        for i_task in range(NUMBER_OF_SHARED_COMPLETED_TASKS):
            Task.objects.create(
                title=f"Completed shared task {i_task}",
                author=cls.new_user,
                body=f"Completed shared task {i_task} body",
                category=category,
                is_completed=True,
            )
        # Add completed user private tasks
        for i_task in range(NUMBER_OF_USER_PRIVATE_COMPLETED_TASKS):
            Task.objects.create(
                title=f"Completed private task {i_task} of {cls.new_user.username}",
                author=cls.new_user,
                body=f"Completed private task {i_task} body",
                category=category,
                is_completed=True,
                is_private=True,
            )
        # Add active private user tasks
        for i_task in range(NUMBER_OF_USER_PRIVATE_TASKS):
            Task.objects.create(
                title=f"Private task {i_task} of {cls.new_user.username}",
                author=cls.new_user,
                body=f"Private task {i_task} body",
                category=category,
                is_private=True,
                is_completed=False,
            )
        # Add archived shared tasks
        for i_task in range(NUMBER_OF_ARCHIVED_SHARED_TASKS):
            Task.objects.create(
                title=f"Archived shared task {i_task}",
                author=cls.new_user,
                body=f"Archived shared task {i_task} body",
                category=category,
                is_private=False,
                is_archived=True,
            )

    def test_home_url(self):
        """
        Ensure "journal:task_list" view is not accessible without login.
        """
        # Redirect when not logged in
        url = reverse("journal:task_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_correct_login(self):
        """
        Check login for `testuser`.
        After login must be redirected to task list view.
        """
        url = reverse("login")
        response = self.client.post(
            url, {"username": self.username, "password": self.password}, follow=True
        )
        self.assertContains(response, "Журнал Дежурства")
        self.assertContains(response, "задачи")

    def test_task_list_view_task_count(self):
        """
        Check number of tasks shown in "journal:task_list" view.
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(
            url, {"username": self.username, "password": self.password}, follow=True
        )
        # Go to list page
        url = reverse("journal:task_list")
        response = self.client.get(url)
        # Check tasks count on the page
        self.assertEqual(len(response.context["task_list"]), TOTAL_ACTIVE_USER_TASKS)

    def test_task_list_view_task_count_with_hide_private_filter(self):
        """
        Check number of tasks shown in "journal:task_list" view with "?hide_private" GET parameter.
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(
            url, {"username": self.username, "password": self.password}, follow=True
        )
        # Go to list page with "hide private" filter = true
        url = reverse("journal:task_list") + "?hide_private=true"
        response = self.client.get(url)
        # Check tasks count on the page
        self.assertEqual(len(response.context["task_list"]), NUMBER_OF_SHARED_TASKS)

        # Go to list page with "hide private" filter = false
        url = reverse("journal:task_list") + "?hide_private=false"
        response = self.client.get(url)
        # Check tasks count on the page
        self.assertEqual(
            len(response.context["task_list"]),
            NUMBER_OF_SHARED_TASKS + NUMBER_OF_USER_PRIVATE_TASKS,
        )

    def test_task_list_view_private_task_count(self):
        """
        Check number of private tasks shown in "journal:private_task_list" view.
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(
            url, {"username": self.username, "password": self.password}, follow=True
        )
        # Go to private task list page
        url = reverse("journal:private_task_list")
        response = self.client.get(url)
        # Check tasks count on the page
        self.assertEqual(
            len(response.context["private_task_list"]), NUMBER_OF_USER_PRIVATE_TASKS
        )

    def test_task_list_view_completed_task_count(self):
        """
        Check number of completed tasks shown in "journal:completed_task_list" view.
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(
            url, {"username": self.username, "password": self.password}, follow=True
        )
        # Go to private task list page
        url = reverse("journal:completed_task_list")
        response = self.client.get(url)
        # Check tasks count on the page
        self.assertEqual(
            len(response.context["completed_task_list"]), TOTAL_COMPLETED_USER_TASKS
        )

    def test_task_list_view_favorite_task_count(self):
        """
        Check number of favorite tasks shown in "journal:favorite_task_list" view.
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(
            url, {"username": self.username, "password": self.password}, follow=True
        )
        # Go to private task list page
        url = reverse("journal:favorite_task_list")
        response = self.client.get(url)
        # Check tasks count on the page - nothing is favorited:
        self.assertEqual(len(response.context["favorite_task_list"]), 0)

        # Add one normal task and one archived to favorites and test again:
        task = Task.objects.filter(is_archived=False).first()
        task.users_favorited.add(self.new_user)

        archived_task = Task.objects.filter(is_archived=True).first()
        archived_task.users_favorited.add(self.new_user)

        response = self.client.get(url)
        self.assertEqual(len(response.context["favorite_task_list"]), 1)
