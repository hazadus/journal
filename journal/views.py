from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    """ "Задачи" view in Dashboard  """
    model = Task
    template_name = "task_list.html"
    queryset = Task.active.all()
    context_object_name = "task_list"


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "task_detail.html"
    context_object_name = "task"
