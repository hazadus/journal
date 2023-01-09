from django.db import models
from django.conf import settings


class ActiveTaskManager(models.Manager):
    """
    Used to retrieve only not completed, archived, or private tasks with 'Task.active.all() notation.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_private=False, is_archived=False, is_completed=False)


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
    users_acquainted = models.ManyToManyField(verbose_name="Ознакомлены", to=settings.AUTH_USER_MODEL,
                                              related_name="tasks_acquainted", blank=True)

    # Model Managers
    objects = models.Manager()
    active = ActiveTaskManager()

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created"]

    def __str__(self):
        return self.title