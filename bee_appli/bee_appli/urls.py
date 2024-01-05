from django.contrib import admin
from django.urls import include, path
from .settings import DEBUG

urlpatterns = [
    path("admin/", admin.site.urls),
    #    path("hive/", include("hive.urls"))
]

# Needed to show the sidebar in admin when in debug mode
if DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(r"__debug__/", include(debug_toolbar.urls)),
    ]
