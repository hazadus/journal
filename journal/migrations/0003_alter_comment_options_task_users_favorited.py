# Generated by Django 4.1.5 on 2023-01-15 10:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("journal", "0002_alter_taskcategory_options_comment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "ordering": ["created"],
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
        migrations.AddField(
            model_name="task",
            name="users_favorited",
            field=models.ManyToManyField(
                blank=True,
                related_name="tasks_favorited",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Добавили в избранное",
            ),
        ),
    ]
