# Generated by Django 4.1.5 on 2023-01-21 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0004_report"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="completed",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Завершена"),
        ),
    ]
