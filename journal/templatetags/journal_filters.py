from django import template

register = template.Library()


@register.filter(name="new_comments_count_for_user")
def new_comments_count_for_user(value, arg):
    """
    Returns count of comments for the task with which `user` is not acquinted.
    """
    task = value
    user = arg
    new_comments_count = 0

    for comment in task.comments.all():
        if not comment.is_archived:
            if user not in comment.users_acquainted.all():
                new_comments_count += 1

    return new_comments_count


@register.filter(name="is_user_acquainted")
def is_user_acquainted(value, arg):
    """
    Returns True if `user` is acquainted with task and all of its comments. Otherwise, returns False.
    """
    task = value
    user = arg

    if user not in task.users_acquainted.all():
        return False

    for comment in task.comments.all():
        if not comment.is_archived:
            if user not in comment.users_acquainted.all():
                return False

    return True


@register.filter(name="is_users_favorite")
def is_users_favorite(value, arg):
    """
    Returns True if `user` added this task to favorites. Otherwise, returns False.
    """
    task = value
    user = arg

    if user not in task.users_favorited.all():
        return False

    return True
