from django.db.models import QuerySet
from django.utils.html import escapejs


def task_to_js_object(task):
    """
    TODO: docstrings
    """
    return f'''
    {{
        "pk": "{task.pk}",
        "title": "{escapejs(task.title)}",
        "category": "{escapejs(task.category)}",
        "category_id": "{task.category.id}",
        "url": "{ task.get_absolute_url() }",
        "is_favorite": {"true" if task.is_favorite else "false"},
        "is_private": {"true" if task.is_private else "false"},
        "is_acquainted": {"true" if task.is_acquainted else "false"},
        "is_completed": {"true" if task.is_completed else "false"},
        "comments_count": { task.comments_count },
        "new_comments_count": { task.new_comments_count if task.new_comments_count else "0" },
        "created": "{ task.created.isoformat() }",
        "completed": "{ task.completed.isoformat() if task.is_completed else "" }"
    }}
    '''.replace("\n", "")


def category_to_js_object(category):
    """
    TODO: docstrings
    """
    return f'''
    {{
        "id": "{category.pk}",
        "title": "{escapejs(category.title)}"
    }}
    '''.replace("\n", "")


def task_queryset_to_json(tasks: QuerySet):
    """
    TODO: docstrings
    """
    task_list_js = ""

    for task in tasks:
        task_list_js += task_to_js_object(task=task) + ","

    # Cut trailing comma to make json valid
    json = f'"task_list": [ {task_list_js[:-1]} ]'
    return json


def category_queryset_to_json(categories: QuerySet):
    """
    TODO: docstrings
    """
    category_list_js = ""

    for category in categories:
        category_list_js += category_to_js_object(category=category) + ","

    # Cut trailing comma to make json valid
    json = f'"category_list": [ {category_list_js[:-1]} ]'
    return json


def create_task_list_json(tasks: QuerySet, categories: QuerySet, order_by_args: list) -> str:
    """
    TODO: add category list into json
    Creates JSON for Vue frontend consisting of:
    {
        "task_list": [...], - all tasks
        "category_list": [...] - all categories
    }
    """
    if len(order_by_args):
        tasks = tasks.order_by(*order_by_args)

    task_list_json = task_queryset_to_json(tasks=tasks)
    category_list_json = category_queryset_to_json(categories=categories)
    json = f'{{ {task_list_json}, {category_list_json} }}'

    return json
