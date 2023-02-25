from django.urls import path

from .api import logged_in_user_api

app_name = "users"

urlpatterns = [
    # API views
    path("api/v1/logged_in_user/", logged_in_user_api, name="api_logged_in_user"),
]
