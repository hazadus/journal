from django.urls import path

from .views import (TaskListView, PrivateTaskListView, CompletedTaskListView, TaskDetailView, TaskCreateView,
                    comment_add, comment_delete, comment_archive, task_acquaint)

app_name = "journal"

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("tasks/private/", PrivateTaskListView.as_view(), name="private_task_list"),
    path("tasks/completed/", CompletedTaskListView.as_view(), name="completed_task_list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("task/create/", TaskCreateView.as_view(), name="task_create"),
    path("task/<int:pk>/add_comment/", comment_add, name="task_comment_add"),
    path("task/<int:task_pk>/delete_comment/<int:comment_pk>/", comment_delete, name="task_comment_delete"),
    path("task/<int:task_pk>/archive_comment/<int:comment_pk>/", comment_archive, name="task_comment_archive"),
    path("task/<int:pk>/acquaint/", task_acquaint, name="task_acquaint"),
]
