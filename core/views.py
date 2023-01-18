from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Notifications list
    """
    all_notifications = request.user.notifications.all()

    return render(request, "dashboard.html", {
        "all_notifications": all_notifications,
    })
