from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType

from django_project.spawn_redis import redis
from .models import Document, DocumentCategory
from users.models import CustomUser
from core.models import Notification


class DocumentListView(LoginRequiredMixin, ListView):
    """
    Document list view with all active (i.e. not completed, not archived) documents.
    """
    model = Document
    queryset = Document.objects.filter(is_completed=False, is_archived=False)
    template_name = "document_list.html"
    context_object_name = "document_list"

    def get_context_data(self, **kwargs):
        """
        Add all document categories to context.
        """
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get("category_id")

        categories = DocumentCategory.objects.all().annotate(
            document_qty=Count("documents", filter=Q(documents__is_archived=False) & Q(documents__is_completed=False))
        ).order_by("-document_qty")

        document_list = Document.objects.filter(is_archived=False, is_completed=False)
        total_count = document_list.count()

        if category_id:
            document_list = document_list.filter(category_id__exact=category_id)

        context["categories"] = categories
        context["category_id"] = int(category_id) if category_id else None
        context["document_list"] = document_list
        context["total_count"] = total_count
        return context


class DocumentDetailView(LoginRequiredMixin, DetailView):
    """
    Document detail view.
    """
    model = Document
    template_name = "document_detail.html"
    context_object_name = "document"

    def get_context_data(self, **kwargs):
        """
        Add all notifications and views count (from Redis) to context.
        """
        context = super().get_context_data(**kwargs)
        document = context["document"]

        # Get all notifications for this document
        document_notifications = Notification.objects.filter(
            target_object_id=document.pk,
            target_content_type_id=ContentType.objects.get_for_model(document)
        ).order_by("-timestamp")
        context["document_notifications"] = document_notifications

        total_views = redis.incr(f"document:{document.pk}:views")
        context["total_views"] = total_views

        return context


@login_required
@require_POST
def document_acquaint(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Acquaint logged in user with document.
    HTMX view, does the thing, then returns part of a page with document block.
    """
    document = get_object_or_404(Document, pk=pk)
    user = request.user

    # Acquaint
    if user not in document.users_acquainted.all():
        document.users_acquainted.add(user)

    # Notify admins
    Notification.send(sender=request.user, actor=request.user, recipient=CustomUser.objects.filter(is_superuser=True),
                      verb_code=Notification.VERB_CODES.acquainted, target=document)

    return render(request, "snippets/document_detail_item.html", {
        "document": document,
    })
