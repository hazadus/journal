from django.urls import path

from .views import dashboard

app_name = "core"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
]
