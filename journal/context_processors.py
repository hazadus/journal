from django.http import HttpRequest

from .models import Task


def green_tasks(request: HttpRequest) -> dict:
    green_active_tasks = 0
    green_favorite_tasks = 0
    green_completed_tasks = 0

    if request.user.is_authenticated:
        green_active_tasks = Task.get_green_active_tasks(request.user)
        green_favorite_tasks = Task.get_green_favorite_tasks(request.user)
        green_completed_tasks = Task.get_green_completed_tasks(request.user)

    return {
        "green_active_tasks": green_active_tasks,
        "green_favorite_tasks": green_favorite_tasks,
        "green_completed_tasks": green_completed_tasks,
    }