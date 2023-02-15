from django.db.models.expressions import RawSQL
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from django.db.models import Q, Case, When, Value, OuterRef, Subquery, Count

from users.models import CustomUser
from .models import Task, Comment, TaskCategory
from .serializers import TaskSerializer, TaskCategorySerializer


class TaskCategoryListApi(ListModelMixin, GenericAPIView):
    """
    List all task categories
    """
    queryset = TaskCategory.objects.all()
    serializer_class = TaskCategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TaskListApi(ListModelMixin, GenericAPIView):
    """
    List all tasks
    Sorting example: ?orderByFields=-is_favorite,-is_completed,-is_acquainted,-created,-completed
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        task_list = Task.objects.all()

        # Exclude archived tasks
        task_list = task_list.exclude(
            is_archived=True
        )

        # Exclude private tasks of other users
        task_list = task_list.exclude(
            ~Q(author=self.request.user) & Q(is_private=True)
        )

        # Count non-archived comments for each task
        task_list = task_list.annotate(
            comments_count=Count("comments", filter=Q(comments__is_archived=False))
        )

        task_list = task_list.annotate(
            category_title=Subquery(
                TaskCategory.objects.filter(
                    Q(id=OuterRef("category_id"))
                ).values("title")
            )
        )

        task_list = task_list.annotate(
            new_comments_count=RawSQL("""
                    SELECT COUNT(*) AS "__count"
                    FROM "journal_comment"
                    WHERE ("journal_comment"."task_id" IN ("journal_task"."id")
                    AND NOT "journal_comment"."is_archived"
                    AND NOT (EXISTS(SELECT '1' AS "a" FROM "journal_comment_users_acquainted" U1 
                    WHERE (U1."customuser_id" IN (%s) AND U1."comment_id" = ("journal_comment"."id")) LIMIT 1)))
                 """, (self.request.user.pk,))
        )

        # `is_favorite` will be `username` if user favorited the Task, or else None
        task_list = task_list.annotate(
            is_favorite=Subquery(
                CustomUser.objects.filter(
                    Q(tasks_favorited__in=OuterRef("pk")) &
                    Q(tasks_favorited__users_favorited__exact=self.request.user.pk)
                ).values("username")
            )
        )

        # `is_acquinted` will be `username` if user acquainted with Task, or else None
        task_list = task_list.annotate(
            is_acquainted_task=Subquery(
                CustomUser.objects.filter(
                    Q(tasks_acquainted__in=OuterRef("pk")) &
                    Q(tasks_acquainted__users_acquainted__exact=self.request.user.pk)
                ).values("username")
            )
        )

        # `id_latest_comment_unacqainted` will be id of the newest unacquainted comment, or else None
        task_list = task_list.annotate(
            id_latest_comment_unacqainted=Subquery(
                Comment.objects.filter(Q(task_id=OuterRef("pk")) &
                                       ~Q(users_acquainted__exact=self.request.user.pk) &
                                       Q(is_archived=False))
                .order_by("-created")
                .values("id")
            )
        )

        # Finally, annotate with `is_acquainted` based on two previous fields
        task_list = task_list.annotate(
            is_acquainted=Case(
                When(
                    Q(is_acquainted_task=None) | ~Q(id_latest_comment_unacqainted=None),
                    then=Value(False)
                ),
                default=Value(True)
            )
        )

        # Default sorting params:
        order_by_args = ["is_acquainted", "is_completed", "-completed", "-created"]

        # Use sorting parameters passed from frontend:
        order_by_fields = self.request.GET.get("orderByFields")
        if order_by_fields:
            order_by_args = order_by_fields.split(",")

        # Actually define order:
        task_list = task_list.order_by(*order_by_args).select_related("category")

        return task_list

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
