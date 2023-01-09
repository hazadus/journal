from django.contrib import admin

from .models import Task, TaskCategory


@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "created"]
    list_filter = ["is_completed", "is_private", "is_archived", "created"]
    ordering = ["is_completed", "-created"]
