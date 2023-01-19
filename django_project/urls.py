from django.contrib import admin
from django.urls import path, include

import notifications.urls

urlpatterns = [
    path("", include("core.urls")),
    path("journal/", include("journal.urls")),
    path("documents/", include("documents.urls")),
    path("adminpanel/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # Must be "accounts/" to work properly
    # 3rd
    path("inbox/notifications/", include(notifications.urls, namespace="notifications")),
]

# Configure Admin panel titles
admin.site.site_header = "Панель управления Журнала Дежурства"
admin.site.site_title = "Панель управления Журнала Дежурства"
admin.site.index_title = "Управление Журналом Дежурства"
