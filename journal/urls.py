from django.urls import path

from .views import TaskListView, TaskDetailView, TaskCreateView

app_name = "journal"

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("task/create/", TaskCreateView.as_view(), name="task_create"),
]
