# Generated by Django 4.1.5 on 2023-01-19 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="new_body",
            field=models.TextField(blank=True, null=True, verbose_name="New body"),
        ),
        migrations.AddField(
            model_name="notification",
            name="new_title",
            field=models.CharField(
                blank=True, max_length=256, null=True, verbose_name="New title"
            ),
        ),
    ]