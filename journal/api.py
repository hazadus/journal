from django.db.models.expressions import RawSQL
from django.db.models import Q, Case, When, Value, OuterRef, Subquery, Count

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView, get_object_or_404

from users.models import CustomUser
from core.models import Notification
from .models import Task, Comment, TaskCategory
from .serializers import TaskSerializer, TaskDetailSerializer, TaskCategorySerializer, CommentSerializer


class TaskCategoryListAPI(ListAPIView):
    """
    List all task categories.
    """
    queryset = TaskCategory.objects.all()
    serializer_class = TaskCategorySerializer


class TaskListAnnotateMixin(GenericAPIView):
    """
    Annotates Task QuerySet with additional fields depending on logged in user:
    - comments_count, category_title, new_comments_count, is_favorite, is_acquainted, author first/second/last name,
      author avatar url.

    Field list for order_by() should be passed via orderByFields GET parameter.
    Ordering example: ?orderByFields=-is_favorite,-is_completed,-is_acquainted,-created,-completed
    """
    def get_queryset(self):
        """
        Annotate QuerySet. Exclude archived tasks and private tasks of other users.
        Apply `order_by()` based on GET parameters.
        """
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

        # Add category title
        task_list = task_list.annotate(
            category_title=Subquery(
                TaskCategory.objects.filter(
                    Q(id=OuterRef("category_id"))
                ).values("title")
            )
        )

        # Add author info directly to comments:
        task_list = task_list.annotate(
            author_last_name=Subquery(
                CustomUser.objects.filter(
                    Q(pk=OuterRef("author_id"))
                ).values("last_name")
            )
        )
        task_list = task_list.annotate(
            author_first_name=Subquery(
                CustomUser.objects.filter(
                    Q(pk=OuterRef("author_id"))
                ).values("first_name")
            )
        )
        task_list = task_list.annotate(
            author_second_name=Subquery(
                CustomUser.objects.filter(
                    Q(pk=OuterRef("author_id"))
                ).values("second_name")
            )
        )

        # Add author's avatar URL like: "images/v.skutin_profile_pic.jpg"
        task_list = task_list.annotate(
            author_avatar_url=Subquery(
                CustomUser.objects.filter(
                    Q(pk=OuterRef("author_id"))
                ).values("avatar_img")
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


class TaskListAPI(TaskListAnnotateMixin, ListAPIView):
    """
    List all tasks. Less detailed data (no body, no author info).
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskListStatsAPI(TaskListAnnotateMixin, ListAPIView):
    """
    Returns some tasks stats for currently logged in user.
    These stats are used for badges in sidebar.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        """
        Generates task stats for currently logged in user, using annotation mixin.
        By "new" we mean tasks logged in user is not acquainted with, or tasks which have comments logged in user
        is not acquainted with.

        total_new_tasks: total number of "new" tasks.
        active_new_tasks: number of incomplete "new" tasks.
        favorite_new_tasks: number of "new" tasks favorited by user.
        completed_new_tasks: number of completed "new" tasks.
        """
        total_new_tasks = self.get_queryset().filter(
            is_acquainted=False, is_archived=False
        ).count()

        active_new_tasks = self.get_queryset().filter(
            is_acquainted=False, is_completed=False, is_archived=False
        ).count()

        # Favorite tasks are those with `is_favorite != None`, according to our annotation.
        favorite_new_tasks = self.get_queryset().filter(
            Q(is_acquainted=False) & ~Q(is_favorite=None) & Q(is_archived=False)
        ).count()

        completed_new_tasks = self.get_queryset().filter(
            Q(is_acquainted=False) & Q(is_completed=True) & Q(is_archived=False)
        ).count()

        stats = {
            "total_new_tasks": total_new_tasks,
            "active_new_tasks": active_new_tasks,
            "favorite_new_tasks": favorite_new_tasks,
            "completed_new_tasks": completed_new_tasks,
        }
        return Response(stats)


class TaskDetailAPI(TaskListAnnotateMixin, RetrieveAPIView):
    """
    Get one task by its pk. Detailed info including body, author first/second/last name, avatar url.
    """
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


@api_view(http_method_names=['GET'])
def task_toggle_favorite_api(request, pk: int) -> Response:
    """
    Toggle "favorite" status for a task for current user. Send notifications.
    """
    user = request.user
    task = get_object_or_404(Task, pk=pk)

    # Add or remove from logged in user's favorites
    if user not in task.users_favorited.all():
        task.users_favorited.add(user)
        is_favorite = True

        Notification.send(sender=user,
                          actor=user,
                          recipient=CustomUser.objects.filter(is_superuser=True),
                          verb_code=Notification.VERB_CODES.favorites_add,
                          target=task)
    else:
        task.users_favorited.remove(user)
        is_favorite = False

    response = {
        "id": task.pk,
        "username": user.username,
        "is_favorite": is_favorite,
    }
    return Response(response)


class CommentListAPI(ListAPIView):
    """
    List all comments, or filter by task ID. Ordered by "created" by default.
    Comment QuerySets gets annotated with `is_acquainted` boolean field depending on currently logged in user.

    GET parameters:
        taskId - get comments for task width ID equal to taskId
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Annotate QuerySet. Exclude archived comments.
        """
        # Filter non-archived comments only:
        comment_list = Comment.objects.filter(is_archived=False)

        task_id = self.request.GET.get("taskId")
        if task_id:
            comment_list = comment_list.filter(task_id=task_id)

        # `user_acquainted` will be equal to user's `username` if he's acquainted with the comment.
        # Otherwise, it'll be None.
        comment_list = comment_list.annotate(
            user_acquainted=Subquery(
                CustomUser.objects.filter(
                    Q(comments_acquainted__in=OuterRef("pk")) &
                    Q(comments_acquainted__users_acquainted__exact=self.request.user.pk)
                ).values("username")
            )
        )

        # Annotate with `is_acquainted` field using previously generated `user_acquainted`:
        comment_list = comment_list.annotate(
            is_acquainted=Case(
                When(
                    Q(user_acquainted=None), then=Value(False)  # User is not aquainted if there's None.
                ),
                default=Value(True)
            )
        )

        # Add author info directly to comments:
        comment_list = comment_list.annotate(
            author_last_name=Subquery(
                CustomUser.objects.filter(
                    Q(pk=OuterRef("author_id"))
                ).values("last_name")
            )
        )
        comment_list = comment_list.annotate(
            author_first_name=Subquery(
                CustomUser.objects.filter(
                    Q(pk=OuterRef("author_id"))
                ).values("first_name")
            )
        )
        comment_list = comment_list.annotate(
            author_second_name=Subquery(
                CustomUser.objects.filter(
                    Q(pk=OuterRef("author_id"))
                ).values("second_name")
            )
        )

        # Add author's avatar URL like: "images/v.skutin_profile_pic.jpg"
        comment_list = comment_list.annotate(
            author_avatar_url=Subquery(
                CustomUser.objects.filter(
                    Q(pk=OuterRef("author_id"))
                ).values("avatar_img")
            )
        )

        return comment_list
