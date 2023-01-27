from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType

from .models import Document
from users.models import CustomUser
from core.models import Notification


class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    queryset = Document.objects.filter(is_completed=False, is_archived=False)
    template_name = "document_list.html"
    context_object_name = "document_list"


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = Document
    template_name = "document_detail.html"
    context_object_name = "document"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document = context["document"]

        # Get all notifications for this document
        document_notifications = Notification.objects.filter(
            target_object_id=document.pk,
            target_content_type_id=ContentType.objects.get_for_model(document)
        ).order_by("-timestamp")
        context["document_notifications"] = document_notifications

        return context


@login_required
@require_POST
def document_acquaint(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Acquaint logged in user with document
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


@login_required
def documents_green_badge(request: HttpRequest) -> HttpResponse:
    """
    Returns green badges for sidebar with "new" ("green") documents counter.
    HTMX view, badge polls this view and updates itself.
    """
    count = Document.get_green_active_documents(request.user).count()

    return render(request, "snippets/document_green_badge.html", {
        "count": count,
    })
