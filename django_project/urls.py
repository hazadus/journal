import notifications.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
    path("users/", include("users.urls")),
    path("journal/", include("journal.urls")),
    path("documents/", include("documents.urls")),
    path("adminpanel/", admin.site.urls),
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # Must be "accounts/" to work properly
    # 3rd
    path(
        "inbox/notifications/", include(notifications.urls, namespace="notifications")
    ),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configure Admin panel titles
admin.site.site_header = "Панель управления Журнала Дежурства"
admin.site.site_title = "Панель управления Журнала Дежурства"
admin.site.index_title = "Управление Журналом Дежурства"
