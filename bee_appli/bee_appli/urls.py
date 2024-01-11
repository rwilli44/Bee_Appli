from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

# Local imports
from apiary.urls import router
from public_api.urls import public_router
from .settings import DEBUG

urlpatterns = [
    # Custom router for beekeper API
    path("", include((router.urls, "apiary"), namespace="apiary")),
    # Custom router for public API
    path(
        "public_api/",
        include((public_router.urls, "public_api"), namespace="public_api"),
    ),
    # Honeypot fake admin login
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    # Actual admin login
    path("apiaryadminaccessportal/", admin.site.urls),
    # URLs for template-based views
    path("apiary/", include("apiary.urls")),
]

# Needed to show the sidebar in admin when in debug mode
if DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(r"__debug__/", include(debug_toolbar.urls)),
    ]
