from django.contrib import admin

from .models import Task, TaskCategory, Comment, Report


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
    ordering = ["-created"]
    # Which fields to show when editing comment via admin panel:
    readonly_fields = ["created"]
    fieldsets = ((None, {"fields": ("task", "author", "created", "body", "is_archived", "users_acquainted",
                                    "parent_comment",)}),)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "created", "is_completed", "completed"]
    list_filter = ["is_completed", "is_private", "is_archived", "created"]
    ordering = ["is_completed", "-completed", "-created"]
    inlines = [CommentInline]
    readonly_fields = ["created"]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["title", "created"]
    ordering = ["-created"]
    readonly_fields = ["created"]
