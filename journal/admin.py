from django.contrib import admin

from .models import Task, TaskCategory, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["body", "task", "author", "created", "is_archived"]
    list_filter = ["is_archived"]
    ordering = ["task", "-created"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "created", "is_completed"]
    list_filter = ["is_completed", "is_private", "is_archived", "created"]
    ordering = ["is_completed", "-created"]
    inlines = [CommentInline]
