from django.views.generic import ListView, DetailView, CreateView
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


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "category", "body", "is_private", "due_date", "attachment"]
    template_name = "task_create.html"

    def form_valid(self, form):
        task = form.save(commit=False)
        # Associate new Task with logged in user:
        task.author = self.request.user
        task.save()

        return super().form_valid(form)
