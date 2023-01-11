from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from .models import Task, Comment


class TaskListView(LoginRequiredMixin, ListView):
    """ "Задачи" view in Dashboard (all active - without completed and private - tasks) """
    model = Task
    template_name = "task_list.html"
    queryset = Task.active.all()
    context_object_name = "task_list"


class CompletedTaskListView(LoginRequiredMixin, ListView):
    """
    "Задачи" - "Завершенные" view in Dashboard (completed: public tasks, private tasks for this user, archived tasks
    excluded).
    """
    model = Task
    template_name = "task_list_completed.html"
    queryset = Task.objects.filter(is_completed=True, is_archived=False)
    context_object_name = "completed_task_list"

    def get_context_data(self, ** kwargs):
        """
        Exclude private tasks of other users
        """
        context = super().get_context_data(**kwargs)
        completed_task_list = context["completed_task_list"]
        context["completed_task_list"] = completed_task_list.exclude(
            ~Q(author=self.request.user) & Q(is_private=True)
        )
        return context


class PrivateTaskListView(LoginRequiredMixin, ListView):
    """
    "Задачи" - "Личные" view in Dashboard (active private tasks of logged in user)
    """
    model = Task
    template_name = "task_list_private.html"
    queryset = Task.objects.filter(is_completed=False, is_archived=False, is_private=True)
    context_object_name = "private_task_list"

    def get_context_data(self, ** kwargs):
        """
        Filter only tasks of logged in user
        """
        context = super().get_context_data(**kwargs)
        private_task_list = context["private_task_list"]
        context["private_task_list"] = private_task_list.filter(author=self.request.user)
        return context


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
def comment_add(request: HttpRequest, pk: int) -> HttpResponse:
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


@login_required
def comment_delete(request: HttpRequest, task_pk: int, comment_pk: int) -> HttpResponse:
    """
    Only admin can actually DELETE the comment from DB.
    HTMX view, deletes a comment, then returns part of a page with comments block.
    """
    task = get_object_or_404(Task, pk=task_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    # Only allow superuser to actually DELETE comments:
    if request.user.is_superuser:
        comment.delete()

    return render(request, "snippets/task_comments_block.html", {
        "task": task,
    })


@login_required
def comment_archive(request: HttpRequest, task_pk: int, comment_pk: int) -> HttpResponse:
    """
    Archive comment.
    HTMX view, archives a comment, then returns part of a page with comments block.
    """
    task = get_object_or_404(Task, pk=task_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    # Only allow superusers or authors to archive comments:
    if request.user.is_superuser or request.user == comment.author:
        comment.is_archived = True
        comment.save()

    return render(request, "snippets/task_comments_block.html", {
        "task": task,
    })
