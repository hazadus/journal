from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    """
    Consumer dedicated to sending Notifications via WebSockets.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None

    def connect(self):
        """
        Establish connecion and add user to notifications group.
        """
        self.room_group_name = "ws-notifications"

        # Accept the connection
        self.accept()

        # Join notifications group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

    def disconnect(self, close_code):
        """
        Remove user from notifications group on disconnect.
        """
        # Leave notifications group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def notification_created(self, event):
        """
        Send notifications to all users in the group.
        """
        self.send(text_data=event["text"])
