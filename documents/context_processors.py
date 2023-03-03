from django.http import HttpRequest

from .models import Document


def green_documents(request: HttpRequest) -> dict:
    """
    Add quantity of documents logged in user is not acquainted with to the context
    (as `green_active_documents`) for use in sidebar.
    """
    green_active_documents = 0

    if request.user.is_authenticated:
        green_active_documents = Document.get_green_active_documents(request.user)

    return {
        "green_active_documents": green_active_documents,
    }
