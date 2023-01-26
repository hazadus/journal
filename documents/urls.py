from django.urls import path

from .views import DocumentListView, DocumentDetailView, document_acquaint, documents_green_badge


app_name = "documents"

urlpatterns = [
    path("", DocumentListView.as_view(), name="document_list"),
    path("document/<int:pk>/", DocumentDetailView.as_view(), name="document_detail"),
    path("document/acquaint/<int:pk>/", document_acquaint, name="document_acquaint"),  # HTMX view
    path("htmx/green_badge/", documents_green_badge, name="green_badge_htmx"),  # HTMX view
]
