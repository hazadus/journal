from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from .models import Task, Comment


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


@login_required
@require_POST
def comment_add(request: HttpRequest, pk=int) -> HttpResponse:
    """
    Add a comment to the task with id == pk.
    HTMX view, adds a comment, then returns part of a page with comments block.
    """
    task = get_object_or_404(Task, pk=pk)
    new_comment = str(request.POST.get("comment_text")).lstrip().rstrip()

    if new_comment:
        Comment.objects.create(task=task, author=request.user, body=new_comment)

    return render(request, "snippets/task_comments_block.html", {
        "task": task,
    })
