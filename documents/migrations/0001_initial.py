# Generated by Django 4.1.5 on 2023-01-17 09:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=128, verbose_name="Название")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
            ],
            options={
                "verbose_name": "Категория документа",
                "verbose_name_plural": "Категории документов",
                "ordering": ["-title"],
            },
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=256, verbose_name="Название")),
                (
                    "body",
                    models.TextField(blank=True, null=True, verbose_name="Содержание"),
                ),
                (
                    "attachment",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="files/%Y/%m/%d",
                        verbose_name="Приложенный файл",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
                (
                    "completed",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Дата и время завершения"
                    ),
                ),
                (
                    "is_completed",
                    models.BooleanField(default=False, verbose_name="Завершено"),
                ),
                (
                    "is_archived",
                    models.BooleanField(default=False, verbose_name="Архивировано"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="documents.documentcategory",
                        verbose_name="Категория",
                    ),
                ),
                (
                    "users_acquainted",
                    models.ManyToManyField(
                        blank=True,
                        related_name="documents_acquainted",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Ознакомлены",
                    ),
                ),
                (
                    "users_assigned",
                    models.ManyToManyField(
                        blank=True,
                        related_name="documents_assigned",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Ответственные",
                    ),
                ),
                (
                    "users_favorited",
                    models.ManyToManyField(
                        blank=True,
                        related_name="documents_favorited",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Добавили в избранное",
                    ),
                ),
            ],
            options={
                "verbose_name": "Документ",
                "verbose_name_plural": "Документы",
                "ordering": ["-created"],
            },
        ),
    ]
