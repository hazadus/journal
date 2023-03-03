from django.db import models
from django.db.models import Q, QuerySet

from django.urls import reverse
from django.conf import settings


class DocumentCategory(models.Model):
    """
    Defines category of a document.
    """
    title = models.CharField(verbose_name="Название", max_length=128)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)

    class Meta:
        verbose_name = "Категория документа"
        verbose_name_plural = "Категории документов"
        ordering = ["-title"]

    def __str__(self):
        return self.title


class Document(models.Model):
    """
    Описывает "документ". Под документом может подразумеваться письменный приказ, устное поручение,
    справочный материал, график работы и т.п. - некий материал "к руководству", имеющий срок действия.
    """
    author = models.ForeignKey(verbose_name="Автор", to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name="documents_created")
    title = models.CharField(verbose_name="Название", max_length=256)
    category = models.ForeignKey(verbose_name="Категория", to=DocumentCategory, on_delete=models.CASCADE,
                                 related_name="documents")
    body = models.TextField(verbose_name="Содержание", null=True, blank=True)
    attachment = models.FileField(verbose_name="Приложенный файл", null=True, blank=True, upload_to="files/%Y/%m/%d")
    created = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Обновлено", auto_now=True)
    completed = models.DateTimeField(verbose_name="Дата и время завершения", blank=True, null=True)
    is_completed = models.BooleanField(verbose_name="Завершено", default=False)
    is_archived = models.BooleanField(verbose_name="Архивировано", default=False)
    users_acquainted = models.ManyToManyField(verbose_name="Ознакомлены", to=settings.AUTH_USER_MODEL,
                                              related_name="documents_acquainted", blank=True)
    users_assigned = models.ManyToManyField(verbose_name="Ответственные", to=settings.AUTH_USER_MODEL,
                                            related_name="documents_assigned", blank=True)
    users_favorited = models.ManyToManyField(verbose_name="Добавили в избранное", to=settings.AUTH_USER_MODEL,
                                             related_name="documents_favorited", blank=True)

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("documents:document_detail", args=[self.pk])

    @classmethod
    def get_green_active_documents(cls, user) -> QuerySet:
        """
        Get QuerySet with active (not archived, not completed) documents `user` not acquainted with.
        """
        return Document.objects.filter(~Q(users_acquainted__in=[user]),
                                       is_archived=False, is_completed=False)
