# Generated by Django 4.1.5 on 2023-01-20 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0003_alter_comment_options_task_users_favorited"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
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
                    "attachment",
                    models.FileField(upload_to="", verbose_name="Файл отчёта"),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создан"),
                ),
            ],
            options={
                "verbose_name": "Отчёт",
                "verbose_name_plural": "Отчёты",
                "ordering": ["-created"],
            },
        ),
    ]
