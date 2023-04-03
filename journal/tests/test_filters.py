from django.test import TestCase

from journal.models import Comment, Task, TaskCategory
from journal.templatetags.journal_filters import (
    is_user_acquainted,
    is_users_favorite,
    new_comments_count_for_user,
)
from users.models import CustomUser


class TaskModelTest(TestCase):
    """
    Test filters from `journal/templatetags/journal_filters.py`.
    """

    username = "testuser"
    password = "password"
    category_title = "New category"
    task_title = "New task"
    task_body = "New task body content"
    comment_body_active = "Active comment"
    comment_body_archived = "Archived comment"
    task = None
    new_user = None

    @classmethod
    def setUpTestData(cls):
        cls.new_user = CustomUser.objects.create_user(
            cls.username, password=cls.password
        )
        new_category = TaskCategory.objects.create(title=cls.category_title)
        cls.task = Task.objects.create(
            author=cls.new_user,
            title=cls.task_title,
            category=new_category,
            body=cls.task_body,
        )
        # Add one `active` and one `archived` comment to the task:
        active_comment = Comment.objects.create(
            author=cls.new_user,
            task=cls.task,
            body=cls.comment_body_active,
            is_archived=False,
        )
        archived_comment = Comment.objects.create(
            author=cls.new_user,
            task=cls.task,
            body=cls.comment_body_archived,
            is_archived=True,
        )

    def test_new_comments_count_for_user(self):
        """
        Check if `new_comments_count_for_user` filter works properly.
        """
        self.assertEqual(
            new_comments_count_for_user(value=self.task, arg=self.new_user), 1
        )

    def test_is_user_acquainted(self):
        """
        Check if `is_user_acquainted` filter works properly.
        """
        self.assertEqual(is_user_acquainted(value=self.task, arg=self.new_user), False)

        # Add `new_user` to acquainted with the task, then test again:
        self.task.users_acquainted.add(self.new_user)
        self.assertEqual(is_user_acquainted(value=self.task, arg=self.new_user), False)
        # Add `new_user` to acquainted with the comment, then test again:
        self.task.comments.filter(is_archived=False).first().users_acquainted.add(
            self.new_user
        )
        self.assertEqual(is_user_acquainted(value=self.task, arg=self.new_user), True)

    def test_is_users_favorite(self):
        """
        Check if `is_users_favorite` filter works properly.
        """
        self.assertEqual(is_users_favorite(value=self.task, arg=self.new_user), False)
        self.task.users_favorited.add(self.new_user)
        self.assertEqual(is_users_favorite(value=self.task, arg=self.new_user), True)
