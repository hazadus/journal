from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("journal.urls")),
    path("documents/", include("documents.urls")),
    path("adminpanel/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # Must be "accounts/" to work properly
]

# Configure Admin panel titles
admin.site.site_header = "Панель управления Журнала Дежурства"
admin.site.site_title = "Панель управления Журнала Дежурства"
admin.site.index_title = "Управление Журналом Дежурства"
