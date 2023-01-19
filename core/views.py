from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Notifications list
    """
    all_notifications = request.user.notifications.all()
    paginator = Paginator(all_notifications, 20)

    # page = number of desired page
    page = request.GET.get("page")

    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        # Deliver first page (works if there's no 'page' parameter at all)
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)

    return render(request, "dashboard.html", {
        "notifications": notifications,
        "paginator": paginator,
        "page_obj": notifications,
    })
