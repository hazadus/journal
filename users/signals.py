from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_logged_out

from .models import CustomUser
from core.models import Notification


@receiver(user_logged_in)
def _user_logged_in(request, user, **kwargs) -> None:
    Notification.send(sender=user, actor=user, recipient=CustomUser.objects.filter(is_superuser=True),
                      verb_code=Notification.VERB_CODES.user_logged_in)


@receiver(user_logged_out)
def _user_logged_out(request, user, **kwargs) -> None:
    Notification.send(sender=user, actor=user, recipient=CustomUser.objects.filter(is_superuser=True),
                      verb_code=Notification.VERB_CODES.user_logged_out)
