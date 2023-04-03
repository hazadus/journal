from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver

from core.models import Notification

from .models import CustomUser


@receiver(user_logged_in)
def _user_logged_in(request, user, **kwargs) -> None:
    """
    Send notifications to superusers when user logs in.
    """
    Notification.send(
        sender=user,
        actor=user,
        recipient=CustomUser.objects.filter(is_superuser=True),
        verb_code=Notification.VERB_CODES.user_logged_in,
    )


@receiver(user_logged_out)
def _user_logged_out(request, user, **kwargs) -> None:
    """
    Send notifications to superusers when user logs out.
    """
    Notification.send(
        sender=user,
        actor=user,
        recipient=CustomUser.objects.filter(is_superuser=True),
        verb_code=Notification.VERB_CODES.user_logged_out,
    )
