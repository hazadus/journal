# Generated by Django 4.1.5 on 2023-04-03 18:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0002_notification_new_body_notification_new_title"),
    ]

    operations = [
        migrations.CreateModel(
            name="File",
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
                    "file",
                    models.FileField(upload_to="files/%Y/%m/%d", verbose_name="Файл"),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создан"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлён"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
            ],
            options={
                "verbose_name": "Файл",
                "verbose_name_plural": "Файлы",
                "ordering": ["-created"],
            },
        ),
    ]