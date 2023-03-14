from django.utils import timezone
from django.db.models.expressions import RawSQL
from django.db.models import Q, Case, When, Value, OuterRef, Subquery, Count

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView, get_object_or_404

from users.models import CustomUser
from core.models import Notification
from .models import Task, Comment, TaskCategory
from .serializers import (
    TaskSerializer, TaskDetailSerializer, TaskCategorySerializer, CommentSerializer, CommentCreateSerializer,
    CommentEditSerializer
)


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
def task_toggle_favorite_api(request: Request, pk: int) -> Response:
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


@api_view(http_method_names=["POST"])
def comment_create_api(request: Request) -> Response:
    """
    Create comment for the task.
    References: https://www.django-rest-framework.org/tutorial/2-requests-and-responses/

    Front end should post object like this:
    {'newComment': {'task': 120, 'author': 2, 'body': 'New comment'}, 'isCompleteTask': False}
    task - task id.
    author - author id.
    body - the comment itself.
    isCompleteTask - whether we need to mark 'task' as completed.
    """
    serializer = CommentCreateSerializer(data=request.data["newComment"])

    if serializer.is_valid():
        comment = serializer.save()
        task = comment.task

        # Mark task as completed if needed
        if request.data["isCompleteTask"]:
            task.is_completed = True
            task.completed = timezone.now()
            task.save()

        # Self-acquaint author
        author = CustomUser.objects.get(pk=request.data["newComment"]["author"])
        comment.users_acquainted.add(author)

        # Send notifications
        # Decide who we will notify
        recipient = task.author if task.is_private else CustomUser.objects.all()

        # Notify about new comment
        Notification.send(sender=request.user, actor=request.user, recipient=recipient,
                          verb_code=Notification.VERB_CODES.comment_add, action_object=comment, target=task)

        # Notify about completed task
        if task.is_completed:
            Notification.send(sender=request.user, actor=request.user, recipient=recipient,
                              verb_code=Notification.VERB_CODES.task_completed, target=task)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=["POST"])
def comment_edit_api(request: Request, pk: int) -> Response:
    """
    Edit a comment. Create notifictions including previous version of the comment.
    Editing only allowed to author, admin, and only if the comment's task is not completed.

    POST /journal/tasks/api/v1/comment/560/edit/
    { 'body': 'New body content' }
    """
    serializer = CommentEditSerializer(data=request.data)

    if serializer.is_valid():
        comment = get_object_or_404(Comment, pk=pk)
        task = comment.task
        user = request.user

        updated_comment_text = serializer.data["body"]
        updated_comment_text = updated_comment_text.lstrip().rstrip()

        can_edit = True if (user.is_superuser or comment.author == user) and not task.is_completed else False

        if comment.body != updated_comment_text and can_edit:
            previous_body = comment.body
            comment.body = updated_comment_text
            comment.save()

            # Decide who we will notify
            recipient = task.author if task.is_private else CustomUser.objects.all()

            # Notify about comment edit
            Notification.send(sender=user, actor=user, recipient=recipient,
                              verb_code=Notification.VERB_CODES.comment_edit, target=comment,
                              previous_body=previous_body, new_body=comment.body)

            return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=["GET"])
def task_acquaint_api(request: Request, pk: int) -> Response:
    """
    Acquaint current user with task and all it's comments.
    """
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    # Acquaint
    if user not in task.users_acquainted.all():
        task.users_acquainted.add(user)

    for comment in task.comments.all():
        if user not in comment.users_acquainted.all():
            comment.users_acquainted.add(user)

    # Notify admins
    Notification.send(sender=request.user, actor=request.user,
                      recipient=CustomUser.objects.filter(is_superuser=True),
                      verb_code=Notification.VERB_CODES.acquainted, target=task)

    response = {
        "username": user.username,
        "task_id": task.pk,
        "status": "User '{username}' acquainted with task '{task_title}'.".format(
            username=user.username,
            task_title=task.title,
        )
    }
    return Response(response)
