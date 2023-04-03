from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CustomUserSerializer


@api_view(http_method_names=["GET"])
def logged_in_user_api(request) -> Response:
    """
    Get CustomUser data for currently logged in user.
    """
    return Response(
        CustomUserSerializer(
            instance=request.user,
        ).data
    )
