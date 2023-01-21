from typing import Any

from django.db import models

from model_utils import Choices
from notifications.signals import notify
from notifications.base.models import AbstractNotification


class Notification(AbstractNotification):
    VERB_CODES = Choices("favorites_add", "task_add", "task_edit", "task_completed", "comment_add", "acquainted",
                         "report_add")

    verb_code = models.CharField(verbose_name="Verb code", max_length=32, null=True, blank=True)
    previous_title = models.CharField(verbose_name="Previous title", max_length=256, null=True, blank=True)
    new_title = models.CharField(verbose_name="New title", max_length=256, null=True, blank=True)
    previous_body = models.TextField(verbose_name="Previous body", null=True, blank=True)
    new_body = models.TextField(verbose_name="New body", null=True, blank=True)

    class Meta(AbstractNotification.Meta):
        abstract = False

    @classmethod
    def add_custom_fields(cls, send_result:  list | list[tuple[Any | None, Any]],
                          verb_code: str, previous_title: str = None, previous_body: str = None,
                          new_title: str = None, new_body: str = None) -> None:
        """
        Add values to our custom model fields.

        :param send_result: pass here what notify.send() have returned
        :param verb_code: one of Notification.VERB_CODES
        :param previous_title: previous title of edited task
        :param new_title: new (updated) title of edited task
        :param previous_body: previous body of edited task or comment
        :param new_body: new (updated) body of edited task or comment
        """
        (receiver, notifications_list) = send_result[0]
        for i_notify in notifications_list:
            i_notify.verb_code = verb_code
            i_notify.previous_title = previous_title
            i_notify.previous_body = previous_body
            i_notify.new_title = new_title
            i_notify.new_body = new_body
            i_notify.save()

    @classmethod
    def send(cls, sender, actor, recipient, verb_code, action_object=None, target=None, previous_title=None,
             previous_body=None, new_title: str = None, new_body: str = None) -> None:
        """
        Custom wrapper for notify.send()
        """
        verbs = {
            Notification.VERB_CODES.task_add: "создаёт задачу",
            Notification.VERB_CODES.task_edit: "изменяет задачу",
            Notification.VERB_CODES.task_completed: "завершает задачу",
            Notification.VERB_CODES.comment_add: "добавляет комментарий",
            Notification.VERB_CODES.acquainted: "ознакамливается",
            Notification.VERB_CODES.favorites_add: "добавляет в избранное",
            Notification.VERB_CODES.report_add: "Сгенерирован отчёт",
        }

        result = notify.send(sender=sender,
                             actor=actor,
                             recipient=recipient,
                             verb=verbs[verb_code],
                             action_object=action_object,
                             target=target)
        Notification.add_custom_fields(send_result=result,
                                       verb_code=verb_code,
                                       previous_title=previous_title,
                                       previous_body=previous_body,
                                       new_title=new_title,
                                       new_body=new_body)