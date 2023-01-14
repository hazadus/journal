from django.http import HttpRequest, HttpResponse
from django.db.models import Q, OuterRef, Subquery
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView

from .models import Task, Comment


class TaskListFilterMixin(ListView):
    """
    Filter task list depending on GET parameters or session settings
    ?hide_private=true - exclude private tasks
    ?hide_private=false - reset option
    """
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        task_list = context[self.context_object_name]

        get_hide_private = self.request.GET.get("hide_private")

        # If not in GET params, check the session params:
        if not get_hide_private:
            get_hide_private = self.request.session.get("hide_private")

        if get_hide_private:
            # Save param in session
            self.request.session["hide_private"] = get_hide_private
            if get_hide_private == "true":
                context["get_hide_private"] = True
                context[self.context_object_name] = task_list.exclude(Q(is_private=True))
            elif get_hide_private == "false":
                context["get_hide_private"] = False

        return context


class TaskListOrderMixin(ListView):
    """
    Order task list depending on GET parameters or session settings
    ?order_by=latest_comment (default)
    ?order_by=created
    """
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(**kwargs)
        task_list = context[self.context_object_name]

        order_by = self.request.GET.get("order_by")

        # If not in GET params, check the session params:
        if not order_by:
            order_by = self.request.session.get("order_by")

        # If nothing in session, set default value:
        if not order_by:
            order_by = "latest_comment"

        # Save param in session
        self.request.session["order_by"] = order_by
        context["order_by"] = order_by

        if order_by == "latest_comment":
            task_list = task_list.annotate(
                last_comment_datetime=Subquery(
                    Comment.objects
                    .filter(task_id=OuterRef("pk"))
                    .order_by("-created")
                    .values("created")
                )
            ).order_by("-last_comment_datetime", "-created")
        elif order_by == "created":
            task_list = task_list.order_by("-created")

        context[self.context_object_name] = task_list
        return context


class TaskListView(LoginRequiredMixin, TaskListFilterMixin, TaskListOrderMixin, ListView):
    """ "Задачи" view in Dashboard (all active - without completed - tasks) """
    model = Task
    template_name = "task_list.html"
    queryset = Task.objects.filter(is_completed=False, is_archived=False)
    context_object_name = "task_list"

    def get_context_data(self, ** kwargs):
        """
        Exclude private tasks of other users
        """
        context = super().get_context_data(**kwargs)
        task_list = context["task_list"]
        context["task_list"] = task_list.exclude(
            ~Q(author=self.request.user) & Q(is_private=True)
        )
        return context


class CompletedTaskListView(LoginRequiredMixin, TaskListFilterMixin, TaskListOrderMixin, ListView):
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


class PrivateTaskListView(LoginRequiredMixin, TaskListFilterMixin, TaskListOrderMixin, ListView):
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
        # Auto-acquaint author with new task:
        task.users_acquainted.add(self.request.user)

        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ["title", "category", "body", "is_private", "due_date", "attachment"]
    template_name = "task_update.html"
    context_object_name = "task"

    def test_func(self):
        """Only allow author or admin to edit the task."""
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser


@login_required
@require_POST
def comment_add(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Add a comment to the task with id == pk.
    HTMX view, adds a comment, then returns part of a page with comments block.
    """
    task = get_object_or_404(Task, pk=pk)
    new_comment_body = str(request.POST.get("comment_text")).lstrip().rstrip()
    check_complete_task = request.POST.get("check_complete_task")

    if new_comment_body:
        # Create new comment, and auto-acquaint author:
        new_comment = Comment.objects.create(task=task, author=request.user, body=new_comment_body)
        new_comment.users_acquainted.add(request.user)
        # Check if the task must be completed:
        if check_complete_task == "complete":
            task.is_completed = True
            task.save()

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

    # Only allow superusers or authors (if task is not completed) to archive comments:
    if request.user.is_superuser or (request.user == comment.author and not task.is_completed):
        comment.is_archived = True
        comment.save()

    return render(request, "snippets/task_comments_block.html", {
        "task": task,
    })


@login_required
@require_POST
def task_acquaint(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Acquaint logged in user with task and all it's comments
    HTMX view, does the thing, then returns part of a page with comments block.
    """
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    # Acquaint
    if user not in task.users_acquainted.all():
        task.users_acquainted.add(user)

    for comment in task.comments.all():
        if user not in comment.users_acquainted.all():
            comment.users_acquainted.add(user)

    return render(request, "snippets/task_full_block.html", {  # NB: full block, 'cause we gotta update the task too!
        "task": task,
    })


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = "search.html"


@login_required
@require_POST
def task_search(request: HttpRequest) -> HttpResponse:
    """
    Search tasks
    HTMX view
    """
    user = request.user
    search_text = request.POST.get("search")

    # Exclude other user's private tasks, then search the remaining tasks (title, body, comments body)
    found_task_list = Task.objects.exclude(
        ~Q(author=user) & Q(is_private=True)
    ).filter(
        Q(title__contains=search_text) | Q(body__contains=search_text) | Q(comments__body__contains=search_text)
    ).distinct()

    return render(request, "snippets/task_search_results.html", {
        "found_task_list": found_task_list,
        "search_text": search_text,
    })
