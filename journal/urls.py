from django.urls import path

from .views import TaskListView, TaskDetailView, TaskCreateView, comment_add, comment_delete

app_name = "journal"

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("task/create/", TaskCreateView.as_view(), name="task_create"),
    path("task/<int:pk>/addcomment/", comment_add, name="task_comment_add"),
    path("task/<int:task_pk>/deletecomment/<int:comment_pk>/", comment_delete, name="task_comment_delete"),
]
