from django.contrib import admin

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["title", "markdown_link", "created"]
    ordering = ["-created"]
    readonly_fields = ["created", "updated"]
