from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Case, Count, OuterRef, Q, Subquery, Value, When
from django.db.models.expressions import RawSQL
from django.db.models.functions import TruncMonth
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from core.models import Notification
from django_project.spawn_redis import redis
from users.models import CustomUser

from .models import Comment, Report, Task, TaskCategory


class TaskListAnnotateMixin(ListView):
    """
    Annotate Task QuerySet with the following fields:
        comments_count: total number of non-archived comments for the task;
        new_comments_count: number of "new" non-archived comments for logged-in user for the task;
        is_favorite: is task favorited by logged in user (actually equals `username` or None respectively);
        is_acquainted: is logged in user acquainted with the task and all of its non-archived comments, boolean.
    """

    def get_context_data(self, **kwargs):
        """
        Add annotation to QuerySet depending on current user.
        """
        context = super().get_context_data(**kwargs)
        task_list = context[self.context_object_name]

        # Count non-archived comments for each task
        task_list = task_list.annotate(
            comments_count=Count("comments", filter=Q(comments__is_archived=False))
        )

        task_list = task_list.annotate(
            new_comments_count=RawSQL(
                """
                    SELECT COUNT(*) AS "__count"
                    FROM "journal_comment"
                    WHERE ("journal_comment"."task_id" IN ("journal_task"."id")
                    AND NOT "journal_comment"."is_archived"
                    AND NOT (EXISTS(SELECT '1' AS "a" FROM "journal_comment_users_acquainted" U1 
                    WHERE (U1."customuser_id" IN (%s) AND U1."comment_id" = ("journal_comment"."id")) LIMIT 1)))
                 """,
                (self.request.user.pk,),
            )
        )

        # `is_favorite` will be `username` if user favorited the Task, or else None
        task_list = task_list.annotate(
            is_favorite=Subquery(
                CustomUser.objects.filter(
                    Q(tasks_favorited__in=OuterRef("pk"))
                    & Q(tasks_favorited__users_favorited__exact=self.request.user.pk)
                ).values("username")
            )
        )

        # `is_acquinted` will be `username` if user acquainted with Task, or else None
        task_list = task_list.annotate(
            is_acquainted_task=Subquery(
                CustomUser.objects.filter(
                    Q(tasks_acquainted__in=OuterRef("pk"))
                    & Q(tasks_acquainted__users_acquainted__exact=self.request.user.pk)
                ).values("username")
            )
        )

        # `id_latest_comment_unacqainted` will be id of the newest unacquainted comment, or else None
        task_list = task_list.annotate(
            id_latest_comment_unacqainted=Subquery(
                Comment.objects.filter(
                    Q(task_id=OuterRef("pk"))
                    & ~Q(users_acquainted__exact=self.request.user.pk)
                    & Q(is_archived=False)
                )
                .order_by("-created")
                .values("id")
            )
        )

        # Finally, annotate with `is_acquainted` based on two previous fields
        task_list = task_list.annotate(
            is_acquainted=Case(
                When(
                    Q(is_acquainted_task=None) | ~Q(id_latest_comment_unacqainted=None),
                    then=Value(False),
                ),
                default=Value(True),
            )
        ).select_related("category")

        context[self.context_object_name] = task_list
        return context


class TaskListFilterMixin(ListView):
    """
    Filter task list depending on GET parameters or session settings
    ?hide_private=true - exclude private tasks
    ?hide_private=false - reset option
    """

    def get_context_data(self, **kwargs):
        """
        Apply filters to QuerySet.
        """
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
                context[self.context_object_name] = task_list.exclude(
                    Q(is_private=True)
                )
            elif get_hide_private == "false":
                context["get_hide_private"] = False

        return context


class TaskListOrderMixin(ListView):
    """
    Order task list depending on GET parameters or session settings
    ?order_by=latest_comment (default)
    ?order_by=created
    ?order_by=completed
    """

    def get_context_data(self, **kwargs):
        """
        Apply ordering to QuerySet.
        """
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

        match order_by:
            case "latest_comment":
                task_list = task_list.annotate(
                    last_comment_datetime=Subquery(
                        Comment.objects.filter(task_id=OuterRef("pk"))
                        .order_by("-created")
                        .values("created")
                    )
                ).order_by("-last_comment_datetime", "-created")
            case "created":
                task_list = task_list.order_by("-created")
            case "completed":
                task_list = task_list.order_by("-completed", "-created")

        context[self.context_object_name] = task_list
        return context


class TaskListView(
    LoginRequiredMixin,
    TaskListAnnotateMixin,
    TaskListFilterMixin,
    TaskListOrderMixin,
    ListView,
):
    """
    "Задачи" view in Dashboard (all active - without completed - tasks).
    """

    model = Task
    template_name = "task_list.html"
    queryset = Task.objects.filter(is_completed=False, is_archived=False)
    context_object_name = "task_list"

    def get_context_data(self, **kwargs):
        """
        Exclude private tasks of other users.
        """
        context = super().get_context_data(**kwargs)
        task_list = context["task_list"]
        context["task_list"] = task_list.exclude(
            ~Q(author=self.request.user) & Q(is_private=True)
        )
        return context


class CompletedTaskListView(
    LoginRequiredMixin,
    TaskListAnnotateMixin,
    TaskListFilterMixin,
    TaskListOrderMixin,
    ListView,
):
    """
    "Задачи" - "Завершенные" view in Dashboard (completed: public tasks, private tasks for this user, archived tasks
    excluded).
    """

    model = Task
    template_name = "task_list_completed.html"
    queryset = Task.objects.filter(is_completed=True, is_archived=False)
    context_object_name = "completed_task_list"

    def get_context_data(self, **kwargs):
        """
        Exclude private tasks of other users
        """
        context = super().get_context_data(**kwargs)
        completed_task_list = context["completed_task_list"]
        context["completed_task_list"] = completed_task_list.exclude(
            ~Q(author=self.request.user) & Q(is_private=True)
        )
        return context


class PrivateTaskListView(
    LoginRequiredMixin,
    TaskListAnnotateMixin,
    TaskListFilterMixin,
    TaskListOrderMixin,
    ListView,
):
    """
    "Задачи" - "Личные" view in Dashboard (active private tasks of logged in user)
    """

    model = Task
    template_name = "task_list_private.html"
    queryset = Task.objects.filter(
        is_completed=False, is_archived=False, is_private=True
    )
    context_object_name = "private_task_list"

    def get_context_data(self, **kwargs):
        """
        Filter only tasks of logged in user
        """
        context = super().get_context_data(**kwargs)
        private_task_list = context["private_task_list"]
        context["private_task_list"] = private_task_list.filter(
            author=self.request.user
        )
        return context


class FavoriteTaskListView(
    LoginRequiredMixin,
    TaskListAnnotateMixin,
    TaskListFilterMixin,
    TaskListOrderMixin,
    ListView,
):
    """
    List favorite tasks of current user.
    """

    model = Task
    template_name = "task_list_favorites.html"
    context_object_name = "favorite_task_list"

    def get_context_data(self, **kwargs):
        """
        Filter only tasks favorited by logged in user, excluding archived tasks.
        """
        context = super().get_context_data(**kwargs)
        favorite_task_list = context["favorite_task_list"]
        context["favorite_task_list"] = favorite_task_list.filter(
            users_favorited__in=[self.request.user], is_archived=False
        )
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    """
    Task detail view.
    """

    model = Task
    template_name = "task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        """
        Add `is_favorite` property to task instance.
        Add total views count for the task (from Redis) to context.
        """
        context = super().get_context_data(**kwargs)
        task = context["task"]

        if self.request.user in task.users_favorited.all():
            task.is_favorite = True

        total_views = redis.incr(f"task:{task.pk}:views")
        context["total_views"] = total_views

        context["task"] = task
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    """
    Task create view.
    """

    model = Task
    fields = ["title", "category", "body", "is_private", "due_date", "attachment"]
    template_name = "task_create.html"

    def form_valid(self, form):
        """
        Set logged in user as author of new task. Auto-acquaint author with new task. Create notifications.
        """
        task = form.save(commit=False)
        # Associate new Task with logged in user:
        task.author = self.request.user
        task.save()
        # Auto-acquaint author with new task:
        task.users_acquainted.add(self.request.user)

        # Decide who we will notify
        recipient = task.author if task.is_private else CustomUser.objects.all()

        Notification.send(
            sender=self.request.user,
            actor=self.request.user,
            recipient=recipient,
            verb_code=Notification.VERB_CODES.task_add,
            target=task,
        )

        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Task update view.
    """

    model = Task
    fields = ["title", "category", "body", "is_private", "due_date", "attachment"]
    template_name = "task_update.html"
    context_object_name = "task"

    def test_func(self):
        """Only allow author or admin to edit the task."""
        obj = self.get_object()
        return obj.author == self.request.user or self.request.user.is_superuser

    def form_valid(self, form):
        """
        Create notifications, saving previous and new title and body of the task (if changed).
        """
        # Get updated task from form, but not yet commit it to DB
        updated_task = form.save(commit=False)

        # Create notification, saving previous and new title and body of the task (if changed)
        task = Task.objects.get(pk=updated_task.pk)
        previous_title = None
        new_title = None
        previous_body = None
        new_body = None

        if not task.title == updated_task.title:
            previous_title = task.title
            new_title = updated_task.title
        if not task.body == updated_task.body:
            previous_body = task.body
            new_body = updated_task.body

        # Decide who we will notify
        recipient = task.author if task.is_private else CustomUser.objects.all()

        # Notify only if title or body has changed
        if previous_title or previous_body:
            Notification.send(
                sender=self.request.user,
                actor=self.request.user,
                recipient=recipient,
                verb_code=Notification.VERB_CODES.task_edit,
                target=task,
                previous_title=previous_title,
                previous_body=previous_body,
                new_title=new_title,
                new_body=new_body,
            )

        # Super actually saves updated task to DB
        return super().form_valid(form)


@login_required
@require_POST
def comment_add(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Add the comment to the task with id == pk. Send notifications.
    HTMX view: add the comment, then return part of the page with comments block.
    """
    task = get_object_or_404(Task, pk=pk)
    new_comment_body = str(request.POST.get("comment_text")).lstrip().rstrip()
    check_complete_task = request.POST.get("check_complete_task")

    if new_comment_body:
        # Create new comment, and auto-acquaint author:
        new_comment = Comment.objects.create(
            task=task, author=request.user, body=new_comment_body
        )
        new_comment.users_acquainted.add(request.user)
        # Check if the task must be completed:
        if check_complete_task == "complete":
            task.is_completed = True
            task.completed = timezone.now()
            task.save()

        # Decide who we will notify
        recipient = task.author if task.is_private else CustomUser.objects.all()

        # Notify about new comment
        Notification.send(
            sender=request.user,
            actor=request.user,
            recipient=recipient,
            verb_code=Notification.VERB_CODES.comment_add,
            action_object=new_comment,
            target=task,
        )

        # Notify about completed task
        if task.is_completed:
            Notification.send(
                sender=request.user,
                actor=request.user,
                recipient=recipient,
                verb_code=Notification.VERB_CODES.task_completed,
                target=task,
            )

    return render(
        request,
        "snippets/task_comments_block.html",
        {
            "task": task,
        },
    )


@login_required
def comment_delete(request: HttpRequest, task_pk: int, comment_pk: int) -> HttpResponse:
    """
    Only admin can actually DELETE the comment from DB.
    HTMX view: delete the comment, then return part of the page with comments block.
    """
    task = get_object_or_404(Task, pk=task_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    # Only allow superuser to actually DELETE comments:
    if request.user.is_superuser:
        comment.delete()

    return render(
        request,
        "snippets/task_comments_block.html",
        {
            "task": task,
        },
    )


@login_required
def comment_archive(
    request: HttpRequest, task_pk: int, comment_pk: int
) -> HttpResponse:
    """
    Archive comment ("archive" is kind of "soft delete" - removes comment from all views, but leaves it in DB).
    HTMX view: archive the comment, then return part of the page with comments block.
    """
    task = get_object_or_404(Task, pk=task_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    # Only allow superusers or authors (if task is not completed) to archive comments:
    if request.user.is_superuser or (
        request.user == comment.author and not task.is_completed
    ):
        comment.is_archived = True
        comment.save()

    return render(
        request,
        "snippets/task_comments_block.html",
        {
            "task": task,
        },
    )


@login_required
def comment_edit(request: HttpRequest, comment_pk: int) -> HttpResponse:
    """
    Inline edit comment.
    HTMX view: return comment "card" HTML block with text input area.
    """
    comment = get_object_or_404(Comment, pk=comment_pk)

    return render(
        request,
        "snippets/task_comment_edit.html",
        {
            "comment": comment,
        },
    )


@login_required
def comment_show(request: HttpRequest, comment_pk: int) -> HttpResponse:
    """
    Show single comment.
    HTMX view, used for "Cancel" button in `comment_edit` view.
    """
    comment = get_object_or_404(Comment, pk=comment_pk)

    return render(
        request,
        "snippets/task_comment_show.html",
        {
            "comment": comment,
        },
    )


@login_required
@require_POST
def comment_edit_save(request: HttpRequest, comment_pk: int) -> HttpResponse:
    """
    Save updated comment. Send notifications.
    HTMX view: return single comment "card-body" HTML block.
    """
    comment = get_object_or_404(Comment, pk=comment_pk)
    task = comment.task
    user = request.user

    updated_comment_text = request.POST.get("updated_comment_text")
    updated_comment_text = updated_comment_text.lstrip().rstrip()

    can_edit = (
        True
        if (user.is_superuser or comment.author == user) and not task.is_completed
        else False
    )

    if comment.body != updated_comment_text and can_edit:
        previous_body = comment.body
        comment.body = updated_comment_text
        comment.save()

        # Decide who we will notify
        recipient = task.author if task.is_private else CustomUser.objects.all()

        # Notify about comment edit
        Notification.send(
            sender=user,
            actor=user,
            recipient=recipient,
            verb_code=Notification.VERB_CODES.comment_edit,
            target=comment,
            previous_body=previous_body,
            new_body=comment.body,
        )

    return render(
        request,
        "snippets/task_comment_show.html",
        {
            "comment": comment,
        },
    )


@login_required
@require_POST
def task_acquaint(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Acquaint logged in user with task and all of it's comments. Send notifications.
    HTMX view: do the thing, then return part of the page with comments block.
    """
    task = get_object_or_404(Task, pk=pk)
    user = request.user
    is_favorite = user in task.users_favorited.all()

    # Acquaint
    if user not in task.users_acquainted.all():
        task.users_acquainted.add(user)

    for comment in task.comments.all():
        if user not in comment.users_acquainted.all():
            comment.users_acquainted.add(user)

    # Notify admins
    Notification.send(
        sender=request.user,
        actor=request.user,
        recipient=CustomUser.objects.filter(is_superuser=True),
        verb_code=Notification.VERB_CODES.acquainted,
        target=task,
    )

    return render(
        request,
        "snippets/task_full_block.html",
        {  # NB: full block, 'cause we gotta update the task too!
            "task": task,
            "is_favorite": is_favorite,
        },
    )


class SearchView(LoginRequiredMixin, TemplateView):
    """
    Search results view.
    """

    template_name = "search.html"


@login_required
@require_POST
def task_search(request: HttpRequest) -> HttpResponse:
    """
    Search tasks, excluding other user's private tasks (other than logged in user).
    HTMX view: return part of the page with search results.
    """
    user = request.user
    search_text = request.POST.get("search")

    # Exclude other user's private tasks, then search the remaining tasks (title, body, comments body)
    found_task_list = (
        Task.objects.exclude(~Q(author=user) & Q(is_private=True))
        .filter(
            Q(title__icontains=search_text)
            | Q(body__icontains=search_text)
            | Q(comments__body__icontains=search_text)
        )
        .distinct()
    )

    return render(
        request,
        "snippets/task_search_results.html",
        {
            "found_task_list": found_task_list,
            "search_text": search_text,
        },
    )


@login_required
@require_POST
def task_toggle_favorite(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Add or remove task from logged in user's favorites (i.e. toggles `favorite` status for current user).
    Send notifications.
    HTMX view: do the thing, then return button with another state.
    """
    task = get_object_or_404(Task, pk=pk)
    user = request.user
    is_favorite = False

    # Add or remove from logged in user's favorites
    if user not in task.users_favorited.all():
        task.users_favorited.add(user)
        is_favorite = True

        Notification.send(
            sender=request.user,
            actor=request.user,
            recipient=CustomUser.objects.filter(is_superuser=True),
            verb_code=Notification.VERB_CODES.favorites_add,
            target=task,
        )
    else:
        task.users_favorited.remove(user)
        is_favorite = False

    return render(
        request,
        "snippets/task_list_item_favorite_button.html",
        {
            "task": task,
            "is_favorite": is_favorite,
        },
    )


class ReportListView(LoginRequiredMixin, ListView):
    """
    Report list view.
    """

    model = Report
    template_name = "report_list.html"
    context_object_name = "report_list"

    def get_context_data(self, **kwargs):
        """
        Add dict `reports_by_month` with keys like "Янв, 2023" and lists of reports as values into context.
        """
        context = super().get_context_data(**kwargs)
        report_list = context["report_list"]

        report_list = report_list.annotate(month=TruncMonth("created"))
        months = sorted(set(report_list.values_list("month", flat=True)), reverse=True)

        # Created dict with keys like "Янв, 2023" and lists of reports as key values
        reports_by_month = {}
        for month in months:
            reports = report_list.filter(
                created__year=month.year, created__month=month.month
            )
            dict_key = month.strftime("%b, %Y").capitalize()
            reports_by_month[dict_key] = list(reports)

        context["reports_by_month"] = reports_by_month
        return context


class TableTaskListView(LoginRequiredMixin, TaskListAnnotateMixin, ListView):
    """
    Table task list view (classic, i.e. server-side rendered).
    """

    model = Task
    template_name = "task_list_table.html"
    context_object_name = "task_list"

    def get_context_data(self, **kwargs):
        """
        Exclude other user's private tasks. Apply filters.
        """
        context = super().get_context_data(**kwargs)
        task_list = context["task_list"]
        category = None

        # Exclude private tasks of other users
        task_list = task_list.exclude(~Q(author=self.request.user) & Q(is_private=True))

        category_id = self.request.GET.get("category_id")
        # If not in GET params, check the session params:
        if not category_id:
            category_id = self.request.session.get("category_id")

        if category_id is not None:
            category = TaskCategory.objects.filter(pk=category_id).first()
            if category:
                task_list = task_list.filter(category=category)
                self.request.session["category_id"] = category_id
            if category_id == "0":
                self.request.session["category_id"] = "0"  # id="0" means "all"

        is_completed = self.request.GET.get("is_completed")
        if not is_completed:
            is_completed = self.request.session.get("is_completed")

        # Set default `is_completed` to `false` for all users
        if not is_completed:
            is_completed = "false"

        match is_completed:
            case "true":
                task_list = task_list.filter(is_completed=True)
                self.request.session["is_completed"] = "true"
            case "false":
                task_list = task_list.filter(is_completed=False)
                self.request.session["is_completed"] = "false"
            case "all":
                self.request.session["is_completed"] = "all"

        is_private = self.request.GET.get("is_private")
        if not is_private:
            is_private = self.request.session.get("is_private")

        if is_private:
            match is_private:
                case "true":
                    task_list = task_list.filter(is_private=True)
                    self.request.session["is_private"] = "true"
                case "false":
                    task_list = task_list.exclude(is_private=True)
                    self.request.session["is_private"] = "false"
                case "all":
                    self.request.session["is_private"] = "all"

        task_list = task_list.order_by(
            "is_acquainted", "-is_favorite", "is_completed", "-completed", "-created"
        )

        categories = TaskCategory.objects.all()

        context["task_list"] = task_list
        context["show_category"] = category
        context["category_id"] = category_id if category_id is not None else 0
        context["categories"] = categories
        context["is_completed"] = is_completed
        context["is_private"] = is_private
        return context


class TableTaskListVueView(LoginRequiredMixin, TemplateView):
    """
    View for Vue app.
    """

    template_name = "task_list_table_vue.html"
