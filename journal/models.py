from datetime import date

from django.db import models
from django.urls import reverse
from django.conf import settings

from users.models import CustomUser


class ActiveTaskManager(models.Manager):
    """
    Used to retrieve only not completed, archived, or private tasks with 'Task.active.all() notation.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_private=False, is_archived=False, is_completed=False)


class ActiveCommentManager(models.Manager):
    """
    Used to retrieve only not archived comment.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=False)


class TaskCategory(models.Model):
    title = models.CharField(verbose_name="Название", max_length=128)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)

    class Meta:
        verbose_name = "Категория задачи"
        verbose_name_plural = "Категории задач"
        ordering = ["-title"]

    def __str__(self):
        return self.title


class Task(models.Model):
    author = models.ForeignKey(verbose_name="Автор", to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name="tasks_created")
    title = models.CharField(verbose_name="Название", max_length=256)
    category = models.ForeignKey(verbose_name="Категория", to=TaskCategory, on_delete=models.CASCADE,
                                 related_name="tasks")
    body = models.TextField(verbose_name="Содержание задачи", null=True, blank=True)
    is_private = models.BooleanField(verbose_name="Личная", default=False)
    is_completed = models.BooleanField(verbose_name="Завершена", default=False)
    is_archived = models.BooleanField(verbose_name="Архивирована", default=False)
    attachment = models.FileField(verbose_name="Приложенный файл", null=True, blank=True, upload_to="files/%Y/%m/%d")
    due_date = models.DateField(verbose_name="Срок выполнения", null=True, blank=True)
    created = models.DateTimeField(verbose_name="Создана", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Обновлена", auto_now=True)
    completed = models.DateTimeField(verbose_name="Завершена", null=True, blank=True)
    users_acquainted = models.ManyToManyField(verbose_name="Ознакомлены", to=settings.AUTH_USER_MODEL,
                                              related_name="tasks_acquainted", blank=True)
    users_favorited = models.ManyToManyField(verbose_name="Добавили в избранное", to=settings.AUTH_USER_MODEL,
                                             related_name="tasks_favorited", blank=True)

    # Model Managers
    objects = models.Manager()
    active = ActiveTaskManager()

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("journal:task_detail", args=[self.pk])

    @property
    def active_comments(self):
        """
        Returns only `active`, i.e. not archived, comments.
        """
        return self.comments.filter(is_archived=False)

    @property
    def is_overdue(self):
        return self.due_date < date.today() if self.due_date else False

    @property
    def is_due_today(self):
        return self.due_date == date.today() if self.due_date else False


class Comment(models.Model):
    task = models.ForeignKey(verbose_name="Задача", to=Task, on_delete=models.CASCADE,
                             related_name="comments")
    author = models.ForeignKey(verbose_name="Автор", to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name="comments_created")
    body = models.TextField(verbose_name="Комментарий", null=False, blank=False)
    is_archived = models.BooleanField(verbose_name="Архивирован", default=False)
    parent_comment = models.ForeignKey(verbose_name="Родительский комментарий", to="Comment", null=True, blank=True,
                                       on_delete=models.CASCADE)
    users_acquainted = models.ManyToManyField(verbose_name="Ознакомлены", to=settings.AUTH_USER_MODEL,
                                              related_name="comments_acquainted", blank=True)
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Обновлен", auto_now=True)

    # Model Managers
    objects = models.Manager()
    active = ActiveCommentManager()

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["created"]

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return "{task_detail_link}#comment-{pk}".format(
            task_detail_link=self.task.get_absolute_url(),
            pk=self.pk
        )


class Report(models.Model):
    title = models.CharField(verbose_name="Название", max_length=256)
    attachment = models.FileField(verbose_name="Файл отчёта")
    created = models.DateTimeField(verbose_name="Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Отчёт"
        verbose_name_plural = "Отчёты"
        ordering = ["-created"]

    def __str__(self):
        return self.title
