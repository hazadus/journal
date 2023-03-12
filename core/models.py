import json
from typing import Any

from django.db import models
from django.conf import settings

from model_utils import Choices
from asgiref.sync import async_to_sync
from rest_framework import serializers
from notifications.signals import notify
from channels.layers import get_channel_layer
from notifications.base.models import AbstractNotification

from .tasks import telegram_inform_admin
from users.serializers import CustomUserMinimalSerializer


class Notification(AbstractNotification):
    """
    Custom Notification model for `django-notifications-hq` app.
    Added fields are verb_code, previous_title, new_title, previous_body, new_body.

    Must be used in `settings.py`:
    NOTIFICATIONS_NOTIFICATION_MODEL = "core.Notification"
    """
    VERB_CODES = Choices("favorites_add", "task_add", "task_edit", "task_completed", "comment_add", "comment_edit",
                         "acquainted", "report_add", "user_logged_in", "user_logged_out")

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
        Custom wrapper for notify.send() and telegram_inform_admin() Celery task.
        Create notification(s) for an event: in DB (with additional fields), via Telegram (for admin).
        Also send notification text to all users via WebSockets.
        """
        verbs = {
            Notification.VERB_CODES.task_add: "создаёт задачу",
            Notification.VERB_CODES.task_edit: "изменяет задачу",
            Notification.VERB_CODES.task_completed: "завершает задачу",
            Notification.VERB_CODES.comment_add: "добавляет комментарий",
            Notification.VERB_CODES.comment_edit: "изменяет комментарий",
            Notification.VERB_CODES.acquainted: "ознакамливается",
            Notification.VERB_CODES.favorites_add: "добавляет в избранное",
            Notification.VERB_CODES.report_add: "Сгенерирован отчёт",
            Notification.VERB_CODES.user_logged_in: "входит в программный комплекс",
            Notification.VERB_CODES.user_logged_out: "выходит из программного комплекса",
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

        # Compose telegram message depending on verb and content type
        host = settings.HOST_NAME
        match verb_code:
            case "comment_add":
                message = '{user} {verb} к ' \
                          '<a href="{host}{url}">{target}</a>:\n"{comment}"'.format(
                            host=host,
                            user=actor.short_name,
                            verb=verbs[verb_code],
                            url=target.get_absolute_url(),
                            target=str(target),
                            comment=action_object.body,
                            )
            case "task_add":
                message = '{user} {verb} <a href="{host}{url}">{target}</a>:\n"{task}"'.format(
                    host=host,
                    user=actor.short_name,
                    verb=verbs[verb_code],
                    target=str(target),
                    url=target.get_absolute_url() if target else None,
                    task=target.body,
                )
            case "task_completed" | "acquainted" | "favorites_add":
                message = '{user} {verb} <a href="{host}{url}">{target}</a>'.format(
                    host=host,
                    user=actor.short_name,
                    verb=verbs[verb_code],
                    target=str(target),
                    url=target.get_absolute_url() if target else None
                )
            case "report_add":
                message = '{user} {verb} <a href="{host}{url}">{target}</a>'.format(
                    host=host,
                    user=actor.short_name,
                    verb=verbs[verb_code],
                    target=str(target),
                    url=target.attachment.url
                )
            case "user_logged_in" | "user_logged_out":
                message = '{user} {verb}'.format(
                    user=actor.short_name,
                    verb=verbs[verb_code],
                )
            case _:
                message = '{user} {verb} <a href="{host}{url}">{target}</a>'.format(
                    host=host,
                    user=actor.short_name,
                    verb=verbs[verb_code],
                    target=str(target),
                    url=target.get_absolute_url() if target else None
                )

        # Create Celery task to send Telegram message to admin
        # (excluding notifications generated by admins)
        if not actor.is_superuser or verb_code == "report_add":
            telegram_inform_admin.delay(message)

        # Send all notifications via WebSockets to all connected users
        channel_layer = get_channel_layer()
        group_name = "ws-notifications"
        event = {
            "type": "notification_created",
            "text": "{}",
        }

        # Here we want to iterate over all notifications and send each to corresponding channel (i.e. user)
        # For now, we just send first notification from the list to all connected users.
        (receiver, notifications_list) = result[0]
        if notifications_list:
            serializer = NotificationSerializer(instance=notifications_list[0])
            event["text"] = json.dumps(serializer.data)
            async_to_sync(channel_layer.group_send)(group_name, event)


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    Used to send notification data to users via WebSockets.
    """
    actor = CustomUserMinimalSerializer(many=False, read_only=True)
    recipient = CustomUserMinimalSerializer(many=False, read_only=True)
    action_obj_id = serializers.IntegerField(source="action_object_object_id")
    target_obj_id = serializers.IntegerField(source="target_object_id")

    class Meta:
        model = Notification
        fields = [
            "id",
            "actor",
            "recipient",
            "verb_code",
            "action_obj_id",
            "target_obj_id",
            "timestamp",
        ]
