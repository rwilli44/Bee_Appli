from django.contrib import admin
from django.urls import include, path
from rest_framework import routers


# Local imports
from .settings import DEBUG
from apiary import views

router = routers.DefaultRouter()
router.register(r"beeyards", views.BeeYardViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("apiaryadminaccessportal/", admin.site.urls),
    path("apiary/", include("apiary.urls")),
]

# Needed to show the sidebar in admin when in debug mode
if DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(r"__debug__/", include(debug_toolbar.urls)),
    ]
