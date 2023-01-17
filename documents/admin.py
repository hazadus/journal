from django.contrib import admin

from .models import Document, DocumentCategory


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "created", "is_completed"]
    list_filter = ["is_completed", "is_archived", "created"]
    ordering = ["is_completed", "-created"]
    readonly_fields = ["created"]
