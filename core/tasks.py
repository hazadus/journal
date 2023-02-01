import requests
from celery import shared_task
from django.conf import settings


@shared_task
def telegram_inform_admin(message: str) -> None:
    """
    Sends a message to admin via Telegram bot.
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    admin_chat_id = settings.TELEGRAM_ADMIN_ID

    if bot_token and admin_chat_id:
        request_url = "https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={admin_chat_id}" \
                      "&parse_mode=HTML&text={message}".format(
                            bot_token=bot_token,
                            admin_chat_id=admin_chat_id,
                            message=message
                        )
        request = requests.get(request_url)
