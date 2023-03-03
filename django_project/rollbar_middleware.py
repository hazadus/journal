from rollbar.contrib.django.middleware import RollbarNotifierMiddleware


class CustomRollbarNotifierMiddleware(RollbarNotifierMiddleware):
    """
    Middleware necessary for Rollbar error logging to work.
    Must be added to the list of middlewares in `settings.py` (in production mode).
    """
    def get_payload_data(self, request, exc):
        """
        Add info about logged in user to have more detailed error info in Rollbar logs.
        """
        payload_data = dict()

        if not request.user.is_anonymous:
            # Adding info about the user affected by this event (optional)
            # The 'id' field is required, anything else is optional
            payload_data = {
                'person': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                },
            }

        return payload_data
