from django.views.generic import ListView, DetailView

from .models import Task


class TaskListView(ListView):
    """ "Задачи" view in Dashboard  """
    model = Task
    template_name = "task_list.html"
    queryset = Task.active.all()
    context_object_name = "task_list"


class TaskDetailView(DetailView):
    model = Task
    template_name = "task_detail.html"
    context_object_name = "task"
