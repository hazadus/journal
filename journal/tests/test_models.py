from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from journal.models import Comment, Report, Task, TaskCategory
from users.models import CustomUser


class TaskModelTest(TestCase):
    """
    Test Task, TaskCategory models.
    """

    username = "testuser"
    password = "password"
    category_title = "New category"
    task_title = "New task"
    task_body = "New task body content"
    comment_body_active = "Active comment"
    comment_body_archived = "Archived comment"

    @classmethod
    def setUpTestData(cls):
        new_user = CustomUser.objects.create_user(cls.username, password=cls.password)
        new_category = TaskCategory.objects.create(title=cls.category_title)
        task = Task.objects.create(
            author=new_user,
            title=cls.task_title,
            category=new_category,
            body=cls.task_body,
            due_date=date.today(),
        )
        # Add one `active` and one `archived` comment to the task:
        active_comment = Comment.objects.create(
            author=new_user,
            task=task,
            body=cls.comment_body_active,
            is_archived=False,
        )
        archived_comment = Comment.objects.create(
            author=new_user,
            task=task,
            body=cls.comment_body_archived,
            is_archived=True,
        )

    def test_task_and_category_created(self):
        """
        Ensure that task and category were correctly created.
        """
        task = Task.objects.first()
        self.assertEqual(task.title, self.task_title)
        self.assertEqual(task.body, self.task_body)

        category = TaskCategory.objects.first()
        self.assertEqual(category.title, self.category_title)

    def test_task_and_category_str(self):
        """
        Ensure str representation of the Task, TaskCategory models works as expected.
        """
        task = Task.objects.first()
        self.assertEqual(str(task), self.task_title)

        category = TaskCategory.objects.first()
        self.assertEqual(str(category), self.category_title)

    def test_task_active_comments_property(self):
        """
        Ensure `Task.active_comments` property works as expected.
        :return:
        """
        task = Task.objects.first()
        self.assertEqual(task.active_comments.count(), 1)

    def test_task_is_overdue_and_is_due_today_properties(self):
        """
        Ensure `Task.is_overdue` and `Task.is_due_today` properties work as expected.
        """
        task = Task.objects.first()
        self.assertEqual(task.is_overdue, False)
        self.assertEqual(task.is_due_today, True)

    def test_comment_str(self):
        """
        Check str representation of the comment.
        """
        task = Task.objects.first()
        comment = task.active_comments.first()
        self.assertEqual(str(comment), self.comment_body_active)

    def test_comment_get_absolute_url(self):
        """
        Check `Comment.get_absolute_url()` works as desired.
        """
        task = Task.objects.first()
        comment = task.active_comments.first()
        self.assertEqual(comment.get_absolute_url(), "/journal/task/1/#comment-1")


class ReportModelTest(TestCase):
    """
    Test Report model.
    """

    report_title = "Отчёт о передаче дежурства"

    @classmethod
    def setUpTestData(cls):
        # Content types: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
        report_file = SimpleUploadedFile(
            name="report.xlsx",
            content=b"excel_content",
            content_type="application/octet-stream",
        )

        Report.objects.create(
            title=cls.report_title,
            attachment=report_file,
        )

    def test_report_created(self):
        """
        Ensure that report created correctly.
        """
        report = Report.objects.first()
        self.assertEqual(report.title, self.report_title)

    def test_report_str(self):
        """
        Ensure that str representation of Report works correctly.
        """
        report = Report.objects.first()
        self.assertEqual(str(report), self.report_title)
