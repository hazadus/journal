from django.urls import path

from .views import (TaskListView, PrivateTaskListView, CompletedTaskListView, TaskDetailView, TaskCreateView,
                    TaskUpdateView, comment_add, comment_delete, comment_archive, task_acquaint,
                    SearchView, task_search, FavoriteTaskListView, task_toggle_favorite, task_green_badge)

app_name = "journal"

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/private/", PrivateTaskListView.as_view(), name="private_task_list"),
    path("tasks/completed/", CompletedTaskListView.as_view(), name="completed_task_list"),
    path("tasks/favorites/", FavoriteTaskListView.as_view(), name="favorite_task_list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("task/create/", TaskCreateView.as_view(), name="task_create"),
    path("task/update/<int:pk>/", TaskUpdateView.as_view(), name="task_update"),
    path("task/<int:pk>/add_comment/", comment_add, name="task_comment_add"),
    path("task/<int:task_pk>/delete_comment/<int:comment_pk>/", comment_delete, name="task_comment_delete"),
    path("task/<int:task_pk>/archive_comment/<int:comment_pk>/", comment_archive, name="task_comment_archive"),
    path("task/<int:pk>/acquaint/", task_acquaint, name="task_acquaint"),
    path("task/<int:pk>/favorite/", task_toggle_favorite, name="task_toggle_favorite"),
    path("tasks/search/", SearchView.as_view(), name="task_search"),
    path("tasks/htmx/search/", task_search, name="task_search_htmx"),
    path("tasks/htmx/green_badge/<str:task_type>/", task_green_badge, name="task_green_badge_htmx"),
]
