from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("journal.urls")),
    path("adminpanel/", admin.site.urls),
]
