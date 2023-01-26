from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Notifications list
    Usual + HTMX view
    """
    all_notifications = request.user.notifications.all()
    paginator = Paginator(all_notifications, 5)

    # page = number of desired page
    page = request.GET.get("page")
    # notifications_only = HTMX view requested (only timeline content)
    notifications_only = request.GET.get("notifications_only")

    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        # Deliver first page (works if there's no 'page' parameter at all)
        notifications = paginator.page(1)
    except EmptyPage:
        if notifications_only:
            # Means we reached the end of the feed
            return HttpResponse("")
        notifications = paginator.page(paginator.num_pages)

    template = "snippets/dashboard_timeline_items.html" if notifications_only else "dashboard.html"

    return render(request, template, {
        "notifications": notifications,
        "paginator": paginator,
        "page_obj": notifications,
    })
